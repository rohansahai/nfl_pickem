import pandas as pd
from datetime import datetime as dt
import numpy as np
from util import convert_tz, get_nfl_week_num
from db import get_vi_url, get_local_str, get_prod_str, update


def get_vi_lines(week):
    """
    :param week:
    :return:
    """
    url = get_vi_url(week)
    dfs = pd.read_html(url)
    good_dfs = []
    for df in dfs:
        first_val = df[0].iloc[0]
        if pd.notnull(first_val):
            if 'Game Time' in first_val or first_val.startswith('Week {}'.format(week)):
                good_dfs.append(df)

    if len(good_dfs) > 0:
        spread_df = pd.concat(good_dfs)
        spread_df.drop_duplicates(inplace=True)
    for col, val in [['Time', 'Game Time'], ['Date', 'Week {}'.format(week)]]:
        spread_df[col] = spread_df[0].apply(lambda x: x if val in x else np.nan)
        spread_df[col] = spread_df[col].ffill()
        spread_df[col] = spread_df[col].str.replace(val, '')
        spread_df[col] = spread_df[col].str.strip()

    spread_df = spread_df[spread_df[2].str.startswith('L-') | spread_df[2].str.startswith('W-')]
    spread_df[0] = spread_df[0].str.replace('\d+', '')
    spread_df[0] = spread_df[0].str.strip()

    return spread_df


def fill_in_all_spreads(group):
    """
    :param group:
    :return:
    """
    if any(pd.notnull(group['Spread'])):
        group['reverse_spread'] = 0 - group['Spread'].max()
    else:
        group['reverse_spread'] = np.nan

    return group


def reshape_to_write(group):

    group['home_team_id'] = group['id'].iloc[-1]
    group['away_team_id'] = group['id'].iloc[0]
    group['home_spread'] = group['Spread'].iloc[-1]

    return group


def unpack_game_values(nfl_data, week):
    """
    :param nfl_data:
    :param week:
    :return:
    """
    nfl_data = nfl_data[[0, 4, 'Time', 'Date']]
    nfl_data.columns = ['Teams', 'Spread', 'Time', 'Date']
    nfl_data['week'] = week
    nfl_data = nfl_data.drop(1).reset_index(drop=True)
    nfl_data['DateTime'] = nfl_data['Date'] + ' ' + nfl_data['Time']
    nfl_data['DateTime'] = pd.to_datetime(nfl_data['DateTime'], format='%A %b %d, %Y %I:%M %p')
    nfl_data['time'] = nfl_data['DateTime'].apply(lambda x: convert_tz(x, est_to_utc=True))
    nfl_data.drop(['DateTime', 'Date', 'Time'], axis=1, inplace=True)

    nfl_data.reset_index(inplace=True)
    nfl_data['group_col'] = nfl_data['index'].apply(lambda i: i + 2 if i % 2 == 0 else i + 1)
    nfl_data['Spread'] = nfl_data['Spread'].str.replace('PK', '0')
    nfl_data['Spread'] = nfl_data['Spread'].astype(float)
    nfl_data['Spread'] = nfl_data['Spread'].apply(lambda x: x if x <= 0 else np.nan)
    nfl_data = nfl_data.groupby('group_col').apply(fill_in_all_spreads)
    nfl_data.Spread.fillna(nfl_data.reverse_spread, inplace=True)

    return nfl_data.drop(['index', 'reverse_spread'], axis=1)


def add_team_id(nfl_spreads, prod_str):
    """
    :param nfl_spreads:
    :return:
    """
    team_id_df = pd.read_sql("select id, short_name from team_mapping", prod_str)
    nfl_spreads = pd.merge(nfl_spreads, team_id_df, how='left', left_on='Teams', right_on='short_name')
    nfl_spreads = nfl_spreads.groupby('group_col').apply(reshape_to_write)
    nfl_spreads = nfl_spreads[['week', 'home_team_id', 'away_team_id', 'home_spread', 'time']].drop_duplicates()
    for col in ['created_at', 'updated_at']:
        nfl_spreads[col] = dt.now()
    for col in ['spread_winner_id', 'moneyline_winner_id', 'push', 'home_team_score', 'away_team_score']:
        nfl_spreads[col] = np.nan

    return nfl_spreads


def check_if_spreads_exist(nfl_spreads, week, prod_str):
    """
    :param nfl_spreads:
    :param prod_str:
    :return:
    """
    exist_spreads_df = pd.read_sql("select * from games where week = {}".format(week), prod_str)
    missing_spreads = exist_spreads_df[exist_spreads_df['home_spread'].isnull()]
    if len(missing_spreads) > 0:
        spread_data = nfl_spreads[['home_team_id', 'away_team_id', 'home_spread']]
        update_spreads = pd.merge(missing_spreads, spread_data, how='left', on=['home_team_id', 'away_team_id'])
        for i, row in update_spreads.iterrows():
            update_q = "UPDATE games SET home_spread = {0} WHERE id = {1}".format(row['home_spread_y'], row['id'])
            update(prod_str, update_q)
    elif len(exist_spreads_df) == 0:
        nfl_spreads.to_sql('games', prod_str, if_exists='append', index=False)
    else:
        pass



def add_record(prod_str):
    """
    :return:
    """
    games = pd.read_sql("select * from games where game_status in ('Final', 'Final (OT)')", prod_str)
    games['wins'] = games.groupby('moneyline_winner_id')['id'].transform('count')
    records = games[['moneyline_winner_id', 'wins']].drop_duplicates()
    records.columns = ['id', 'wins']

    games['home_games'] = games.groupby('home_team_id')['home_team_id'].transform('count')
    home_games = games[['home_team_id', 'home_games']].drop_duplicates()
    home_games.columns = ['id', 'home_games']

    games['away_games'] = games.groupby('away_team_id')['away_team_id'].transform('count')
    away_games = games[['away_team_id', 'away_games']].drop_duplicates()
    away_games.columns = ['id', 'away_games']

    total_games = pd.merge(home_games, away_games, how='outer', on='id')
    total_games['total_games'] = total_games['home_games'] + total_games['away_games']

    records = pd.merge(records, total_games[['id', 'total_games']], how='outer', on='id')
    records.fillna(0, inplace=True)
    records['losses'] = records['total_games'] - records['wins']
    records = records[['id', 'wins', 'losses']].drop_duplicates().reset_index(drop=True)

    if not records.empty:
        for i, row in records.iterrows():
            update_q = """UPDATE teams SET wins = {0}, losses = {1} WHERE id = {2}""".format(row['wins'], row['losses'], row['id'])
            for x in range(0, 2):
                while True:
                    try:
                        update(prod_str, update_q)
                    except DatabaseError:
                        continue
                    break


def main():

    prod_str = ENV['ENGINE_STR']
    # prod_str = get_local_str()
    week = get_nfl_week_num()
    nfl_data = get_vi_lines(week)
    nfl_spreads = unpack_game_values(nfl_data, week)
    nfl_spreads = add_team_id(nfl_spreads, prod_str)
    check_if_spreads_exist(nfl_spreads, week, prod_str)
    add_record(prod_str)


if __name__ == '__main__':
    main()
