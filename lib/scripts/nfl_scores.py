import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import numpy as np
from db import update, get_prod_str, get_local_str, get_ff_url
from util import get_nfl_week_num, convert_tz
import random
import time
from datetime import datetime as dt, timedelta as td


def is_there_game_on(current_week, prod_str):
    """
    :param prod_str:
    :return:
    """
    games = pd.read_sql("select time from games where week = {} order by time ASC".format(current_week), prod_str)
    games['start_time'] = games['time'].apply(convert_tz)
    games['end_time'] = games['start_time'] + td(hours=4)
    now = dt.now()
    games['game_happening'] = games.apply(lambda row: 1 if row['start_time'] <= now <= row['end_time'] else 0, axis=1)

    return 1 if any(games['game_happening']) else 0


def get_xml(url):
    """
    returns: Use requests and bs4 to parse the xml
    """
    r = requests.get(url)
    soup = bs(r.text, 'lxml')

    return soup.find_all("table")


def create_score_row(tds):
    """
    returns: Loop through each "td" break in the tables that we've identified in the xml.
    Parse out the team, score, and against spread winner and return a list of lists.
    """
    games = [tds[i:i + 18] for i in range(0, len(tds), 18)]
    scores = []
    for game in games:
        game_row = []
        for i, td in enumerate([game[2:8], game[10:16], game[-1]]):
            if i < 2:
                game_row.extend([td[0].text.strip()] + [x.text.strip() for x in td[1:]])
            else:
                game_row.extend([td.small.text.strip().replace(u'\xa0', u' ')])
        scores.append(game_row)

    return scores


def get_ml_winner(row):
    """
    returns: Identify winner of each game.
    """
    if row['home_team_score'] > row['away_team_score']:
        return row['home_team_id']
    else:
        return row['away_team_id']


def insert_possession_team(row):
    """
    :return:
    """
    game_status = row['game_status']
    down = game_status[10:18]

    if pd.notnull(row['possession']):
        return game_status.replace(down, row['possession'] + ' ').replace('  ', ' ')


def get_weekly_scores(tables, week, prod_str):
    """
    returns: Find all games and build a DataFrame with each game, the scores and the money line
    winner.
    """
    scores = []
    for i, table in enumerate(tables):
        tds = table.find_all('td')
        scores.extend(create_score_row(tds))

    nfl_score_cols = ['away_team_id', 'away_first', 'away_second', 'away_third', 'away_fourth', 'away_ot',
                      'home_team_id', 'home_first', 'home_second', 'home_third', 'home_fourth', 'home_ot',
                      'game_status']
    nfl_scores_df = pd.DataFrame(scores, columns=nfl_score_cols)
    for col in ['away_team_id', 'home_team_id']:
        nfl_scores_df['{}_possession'.format(col)] = nfl_scores_df[col].apply(lambda x: x if '•' in x else 0)
        nfl_scores_df[col] = nfl_scores_df[col].str.replace(' •', '')
    nfl_scores_df['possession'] = nfl_scores_df.apply(lambda row: row['away_team_id_possession']
    if row['away_team_id_possession'] !=0 else row['home_team_id_possession'], axis=1).str.replace(' •', '')
    nfl_scores_df['game_status'] = nfl_scores_df.apply(insert_possession_team, axis=1)

    away_cols = ['away_first', 'away_second', 'away_third', 'away_fourth', 'away_ot']
    home_cols = ['home_first', 'home_second', 'home_third', 'home_fourth', 'home_ot']

    for col in ['away_ot', 'home_ot']:
        nfl_scores_df[col] = nfl_scores_df[col].apply(lambda x: 0 if x == '' else x)

    for col in away_cols + home_cols:
        nfl_scores_df[col] = nfl_scores_df[col].replace('', '0')
        nfl_scores_df[col] = nfl_scores_df[col].astype(int)

    for dir, cols in zip(['away', 'home'], [away_cols, home_cols]):
        nfl_scores_df['{}_team_score'.format(dir)] = nfl_scores_df[cols].sum(axis=1)

    nfl_scores_df['moneyline_winner_id'] = nfl_scores_df.apply(get_ml_winner, axis=1)

    team_id_mapping = pd.read_sql('select last_name, id from team_mapping;', prod_str)
    team_id_mapping = team_id_mapping.set_index('last_name').to_dict()['id']
    for col in ['away_team_id', 'home_team_id', 'moneyline_winner_id']:
        nfl_scores_df[col] = nfl_scores_df[col].map(team_id_mapping)

    nfl_scores_df['week'] = week
    nfl_scores_df['game_live'] = nfl_scores_df['game_status'].apply(lambda x: 0 if x == 'Final' or x == 'OT' else 1)
    keep_cols = ['week', 'home_team_id', 'home_first', 'home_second', 'home_third', 'home_fourth', 'home_ot',
                 'home_team_score', 'away_team_id', 'away_first', 'away_second', 'away_third', 'away_fourth',
                 'away_ot', 'away_team_score', 'moneyline_winner_id', 'game_status', 'game_live']

    return nfl_scores_df[keep_cols]


def calc_spread_winner(row):
    """
    :return:
    """
    spread_home_score = row['home_team_score'] + row['home_spread']
    if spread_home_score > row['away_team_score']:
        spread_winner = row['home_team_id']
        push = False
    elif spread_home_score < row['away_team_score']:
        spread_winner = row['away_team_id']
        push = False
    elif spread_home_score == row['away_team_score']:
        spread_winner = np.nan
        push = True

    row['spread_winner_id'] = spread_winner
    row['push'] = push

    return row


def update_games_with_score(weekly_scores_df, current_week, prod_str):
    """
    :param weekly_scores_df:
    :return:
    """
    exist_games_q = """
    select id, home_team_id, away_team_id, home_spread from games
    where week = {} and spread_winner_id is NULL;""".format(current_week)
    exist_games_df = pd.read_sql(exist_games_q, prod_str)
    weekly_scores_df = pd.merge(weekly_scores_df, exist_games_df, how='left', on=['home_team_id', 'away_team_id'])
    weekly_scores_df = weekly_scores_df[(weekly_scores_df['home_team_score'].notnull()) &
                                        (weekly_scores_df['away_team_score'].notnull()) &
                                        (weekly_scores_df['home_spread'].notnull())]
    weekly_scores_df = weekly_scores_df.apply(calc_spread_winner, axis=1)

    final_games = weekly_scores_df[weekly_scores_df['game_live'] == 0]
    live_game = weekly_scores_df[(weekly_scores_df['game_live'] == 1) & (weekly_scores_df['game_status'].notnull())]
    if len(final_games) > 0:
        for i, row in final_games.iterrows():
            update_q = """
            UPDATE games SET
                spread_winner_id = {0}, moneyline_winner_id = {1}, push = {2},
                home_team_score = {3}, away_team_score = {4}, game_status = '{5}'
            WHERE
                id = {6}""".format(row['spread_winner_id'], row['moneyline_winner_id'],
                                   row['push'], row['home_team_score'], row['away_team_score'],
                                   row['game_status'], row['id'])
            update(prod_str, update_q)
    elif not live_game.empty:
        for i, row in live_game.iterrows():
            update_q = """
            UPDATE games SET
                home_team_score = {0}, away_team_score = {1}, game_status = '{2}'
            WHERE
                id = {3}""".format(row['home_team_score'], row['away_team_score'], row['game_status'], row['id'])
            update(prod_str, update_q)


def determine_result(row):
    """
    :return:
    """
    if row['push'] is True:
        return 'push'
    elif row['winner_id'] == row['spread_winner_id']:
        return 'win'
    elif row['winner_id'] != row['spread_winner_id']:
        return 'loss'


def update_picks_table_with_result(current_week, prod_str):
    """
    :return:
    """
    q = """select picks.id, picks.winner_id, picks.result, games.spread_winner_id, games.push from picks
    LEFT JOIN games on picks.game_id = games.id
    where games.spread_winner_id is not NULL and picks.result is NULL and games.week = {}""".format(current_week)
    results = pd.read_sql(q, prod_str)
    if not results.empty:
        results['result'] = results.apply(determine_result, axis=1)
        for i, row in results.iterrows():
            update_q = """UPDATE picks SET result = '{0}' WHERE id = {1}""".format(row['result'], row['id'])
            update(prod_str, update_q)


def main():

    delay = random.randrange(1, 120)
    time.sleep(delay)
    prod_str = get_prod_str()
    current_week = get_nfl_week_num()
    game_live = is_there_game_on(current_week, prod_str)
    if game_live:
        # prod_str = get_local_str()
        url = get_ff_url(current_week)
        tables = get_xml(url)
        weekly_scores_df = get_weekly_scores(tables, current_week, prod_str)
        update_games_with_score(weekly_scores_df, current_week, prod_str)
        update_picks_table_with_result(current_week, prod_str)


if __name__ == '__main__':
    main()
