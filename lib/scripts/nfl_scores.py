# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import numpy as np
from db import update, get_ff_url
from util import get_nfl_week_num, convert_tz
import random
import time
from datetime import datetime as dt, timedelta as td
from sqlalchemy.exc import DatabaseError
from sqlalchemy import create_engine
import os


def is_there_game_on(current_week, prod_str):
    """
    :return:
    """
    games = pd.read_sql('select time from games where week = {} order by time ASC;'.format(current_week), prod_str)
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


def identify_live_games(row):
    """
    :return:
    """
    if row['game_status'] == 'Final':
        game_live = 0
        game_status = row['game_status']
    elif row['game_status'] == 'OT':
        game_live = 0
        game_status = 'Final (OT)'
    else:
        game_live = 1
        game_status = row['game_status']

    row['game_status'] = game_status
    row['game_live'] = game_live

    return row


def insert_possession_team(row, team_mapping):
    """
    :return:
    """
    if '&' in row['game_status']:
        game_status = row['game_status']
        try:
            i = game_status.index('at') - 1
            down = game_status[10:i]
        except ValueError:
            pass

        if pd.notnull(row['possession']):
            new_status = game_status.replace(down, row['possession'] + ' ').replace('  ', ' ')
            team = new_status.split(' ')[2]
            team_abr = team_mapping[team]
            return new_status.replace(team, team_abr)
    else:
        return row['game_status']


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

    crit = [
        all(nfl_scores_df['away_team_id_possession'] == 0),
        all(nfl_scores_df['home_team_id_possession'] == 0)
    ]

    if not all(crit):
        nfl_scores_df['possession'] = nfl_scores_df.apply(lambda row: row['away_team_id_possession']
        if row['away_team_id_possession'] != 0 else row['home_team_id_possession'], axis=1).str.replace(' •', '')
        team_mapping = pd.read_sql('select team_abr, last_name from team_mapping', prod_str) \
            .set_index('last_name').to_dict()['team_abr']
        nfl_scores_df['game_status'] = nfl_scores_df.apply(lambda row: insert_possession_team(row, team_mapping), axis=1)

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
    nfl_scores_df = nfl_scores_df.apply(identify_live_games, axis=1)
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
    where week = {} and game_status not in ('Final', 'Final (OT)') or game_status is NULL
    and '{}' >= time;""".format(current_week, convert_tz(dt.now(), est_to_utc=True).strftime('%Y-%m-%d %H:%M:%S'))
    exist_games_df = pd.read_sql(exist_games_q, prod_str)
    weekly_scores_df = pd.merge(weekly_scores_df, exist_games_df, how='left', on=['home_team_id', 'away_team_id'])
    weekly_scores_df = weekly_scores_df[(weekly_scores_df['home_team_score'].notnull()) &
                                        (weekly_scores_df['away_team_score'].notnull()) &
                                        (weekly_scores_df['home_spread'].notnull())]
    weekly_scores_df = weekly_scores_df.apply(calc_spread_winner, axis=1)

    final_games = weekly_scores_df[weekly_scores_df['game_live'] == 0]
    live_game = weekly_scores_df[(weekly_scores_df['game_live'] == 1)]
    if len(final_games) > 0:
        for i, row in final_games.iterrows():
            update_q = """
            UPDATE games SET
                spread_winner_id = {0}, moneyline_winner_id = {1}, push = {2},
                home_team_score = {3}, away_team_score = {4}, game_status = '{5}'
            WHERE
                id = {6}""".format(row['spread_winner_id'] if pd.notnull(row['spread_winner_id']) else "NULL",
                                   row['moneyline_winner_id'], row['push'], row['home_team_score'],
                                   row['away_team_score'], row['game_status'], row['id'])
            for x in range(0, 2):
                while True:
                    try:
                        update(prod_str, update_q)
                    except DatabaseError:
                        continue
                    break
    elif not live_game.empty:
        for i, row in live_game.iterrows():
            update_q = """
            UPDATE games SET
                home_team_score = {0}, away_team_score = {1}, game_status = '{2}'
            WHERE
                id = {3}""".format(row['home_team_score'], row['away_team_score'], row['game_status'], row['id'])
            for x in range(0, 2):
                while True:
                    try:
                        update(prod_str, update_q)
                    except DatabaseError:
                        continue
                    break


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
    where games.moneyline_winner_id is not NULL and picks.result is NULL and games.week = {}""".format(current_week)
    results = pd.read_sql(q, prod_str)
    if not results.empty:
        results['result'] = results.apply(determine_result, axis=1)
        for i, row in results.iterrows():
            update_q = """UPDATE picks SET result = '{0}' WHERE id = {1}""".format(row['result'], row['id'])
            for x in range(0, 2):
                while True:
                    try:
                        update(prod_str, update_q)
                    except DatabaseError:
                        continue
                    break


def main():

    prod_str = create_engine(os.environ['ENGINE_STR'])
    current_week = get_nfl_week_num()
    # game_live = is_there_game_on(current_week, prod_str)
    # if game_live:
    #     # prod_str = get_local_str()
    #     delay = random.randrange(1, 120)
    #     time.sleep(delay)
    url = get_ff_url(current_week)
    tables = get_xml(url)
    weekly_scores_df = get_weekly_scores(tables, current_week, prod_str)
    print(weekly_scores_df)
    update_games_with_score(weekly_scores_df, current_week, prod_str)
    update_picks_table_with_result(current_week, prod_str)


if __name__ == '__main__':
    main()
