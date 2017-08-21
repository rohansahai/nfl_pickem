import pandas as pd
from datetime import datetime as dt
import numpy as np


def convert_tz(x, est_to_utc=False):
    """
    :return: Convert utc datetimes to est and remove timezone stamp.
    """
    from dateutil import tz
    if est_to_utc:
        from_zone = tz.gettz('America/New_York')
        to_zone = tz.tzutc()

    else:
        from_zone = tz.tzutc()
        to_zone = tz.gettz('America/New_York')

    try:
        ctz = x.replace(tzinfo=from_zone)
        return ctz.astimezone(to_zone).replace(tzinfo=None)
    except:
        return x


def get_nfl_week_num():
    """
    returns: Use beginning and end dates of 2017 nfl season to map weeks to date ranges.
    Use today's date to determine what week of the season we fall under. Return week (int).
    """
    week_begin = pd.date_range(start='2017-09-14', end='2017-12-29', freq='7D')
    week_end = pd.date_range(start='2017-09-20', end='2018-01-04', freq='7D')
    week_nums = list(range(2, 18))
    week_lol = [[dt(2017, 8, 1), dt(2017, 9, 13), 1]] + [[week_b, week_e, num] for week_b, week_e, num in
                                                         zip(week_begin, week_end, week_nums)]

    today = dt(dt.today().year, dt.today().month, dt.today().day)
    week_mapping_df = pd.DataFrame(week_lol, columns=['Week_Begin', 'Week_End', 'Week_Num'])
    week = week_mapping_df.loc[(week_mapping_df['Week_Begin'] <= today) &
                               (week_mapping_df['Week_End'] >= today)]['Week_Num'].iloc[0]

    return week


def get_vi_lines(week):
    """
    :param week:
    :return:
    """
    url = "http://www.vegasinsider.com/nfl/matchups/matchups.cfm/week/1/season/2017"
    dfs = pd.read_html(url)
    good_dfs = []
    for df in dfs:
        first_val = df[0].iloc[0]
        if pd.notnull(first_val):
            if 'Game Time' in first_val or first_val.startswith('Week {}'.format(week)):
                good_dfs.append(df)

    spread_df = pd.concat(good_dfs)
    spread_df.drop_duplicates(inplace=True)
    for col, val in [['Time', 'Game Time'], ['Date', 'Week {}'.format(week)]]:
        spread_df[col] = spread_df[0].apply(lambda x: x if val in x else np.nan)
        spread_df[col] = spread_df[col].ffill()
        spread_df[col] = spread_df[col].str.replace(val, '')
        spread_df[col] = spread_df[col].str.strip()

    spread_df = spread_df[spread_df[4].notnull()]
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
    nfl_data['Spread'] = nfl_data['Spread'].astype(float)
    nfl_data['Spread'] = nfl_data['Spread'].apply(lambda x: x if x < 0 else np.nan)
    nfl_data = nfl_data.groupby('group_col').apply(fill_in_all_spreads)
    nfl_data.Spread.fillna(nfl_data.reverse_spread, inplace=True)

    return nfl_data.drop(['index', 'reverse_spread'], axis=1)


def add_team_id(nfl_spreads):
    """
    :param nfl_spreads:
    :return:
    """
    team_id_df = pd.read_sql("select id, short_name from teams", ENV['ENGINE_STR'])
    nfl_spreads = pd.merge(nfl_spreads, team_id_df, how='left', left_on='Teams', right_on='short_name')
    nfl_spreads = nfl_spreads.groupby('group_col').apply(reshape_to_write)
    nfl_spreads = nfl_spreads[['week', 'home_team_id', 'away_team_id', 'home_spread', 'time']].drop_duplicates()
    for col in ['created_at', 'updated_at']:
        nfl_spreads[col] = dt.now()
    for col in ['spread_winner_id', 'moneyline_winner_id', 'push', 'home_team_score', 'away_team_score']:
        nfl_spreads[col] = np.nan

    return nfl_spreads


def main():

    week = get_nfl_week_num()
    nfl_data = get_vi_lines(week)
    nfl_spreads = unpack_game_values(nfl_data, week)
    nfl_spreads = add_team_id(nfl_spreads)
    nfl_spreads.to_sql('games', ENV['ENGINE_STR'], if_exists='append', index=False)