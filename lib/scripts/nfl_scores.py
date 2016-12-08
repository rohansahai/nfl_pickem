import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt


def get_nfl_week_num():
    """
    returns: Use beginning and end dates of 2016 nfl season to map weeks to date ranges.
    Use today's date to determine what week of the season we fall under. Return week (int).
    """
    week_begin = pd.date_range(start='2016-09-15', end='2016-12-29', freq='7D')
    week_end = pd.date_range(start='2016-09-21', end='2017-01-02', freq='7D')
    week_nums = list(range(2, 18))
    week_lol = [[dt(2016, 8, 1), dt(2016, 9, 14), 1]] + [[week_b, week_e, num] for week_b, week_e, num in
                                                         zip(week_begin, week_end, week_nums)]

    today = dt(dt.today().year, dt.today().month, dt.today().day)
    week_mapping_df = pd.DataFrame(week_lol, columns=['Week_Begin', 'Week_End', 'Week_Num'])
    week = week_mapping_df.loc[(week_mapping_df['Week_Begin'] <= today) &
                               (week_mapping_df['Week_End'] >= today)]['Week_Num'].iloc[0]

    return week


def get_xml(url):
    """
    returns: Use requests and bs4 to parse the xml from fantasysupercontest.com.
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
                game_row.extend([td[0].contents[0].strip()] + [x.text.strip() for x in td[1:]])
            else:
                game_row.extend([td.small.contents[0].text.strip().replace(u'\xa0', u' ')])
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


def build_team_id_mapping():
    """
    returns: Map sorted teams (descending) to id.
    """
    teams = [
         'Cardinals',
         'Falcons',
         'Ravens',
         'Bills',
         'Panthers',
         'Bears',
         'Bengals',
         'Browns',
         'Cowboys',
         'Broncos',
         'Lions',
         'Packers',
         'Texans',
         'Colts',
         'Jaguars',
         'Chiefs',
         'Rams',
         'Dolphins',
         'Vikings',
         'Patriots',
         'Saints',
         'Giants',
         'Jets',
         'Raiders',
         'Eagles',
         'Steelers',
         'Chargers',
         '49ers',
         'Seahawks',
         'Buccaneers',
         'Titans',
         'Redskins']

    return {team: i+1 for i, team in enumerate(teams)}


def get_weekly_scores(tables, week):
    """
    returns: Find all games and build a DataFrame with each game, the scores and the money line
    winner.
    """
    scores = []
    for i, table in enumerate(tables):
        tds = table.find_all('td')
        scores.extend(create_score_row(tds))

    team_id_mapping = build_team_id_mapping()
    nfl_score_cols = ['away_team_id', 'away_first', 'away_second', 'away_third', 'away_fourth', 'away_ot',
                      'home_team_id', 'home_first', 'home_second', 'home_third', 'home_fourth', 'home_ot', 'game_status']
    nfl_scores_df = pd.DataFrame(scores, columns=nfl_score_cols)

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

    for col in ['away_team_id', 'home_team_id', 'moneyline_winner_id']:
        nfl_scores_df[col] = nfl_scores_df[col].map(team_id_mapping)

    nfl_scores_df['week'] = week
    nfl_scores_df['game_live'] = nfl_scores_df['game_status'].apply(lambda x: 0 if x == 'Final' or x == 'OT' else 1)
    keep_cols = ['week', 'home_team_id', 'home_first', 'home_second', 'home_third', 'home_fourth', 'home_ot',
                 'home_team_score', 'away_team_id', 'away_first', 'away_second', 'away_third', 'away_fourth',
                 'away_ot', 'away_team_score', 'moneyline_winner_id', 'game_status', 'game_live']

    return nfl_scores_df[keep_cols]


def build_yearly_scores():
    """
    :return: Scrape from fleaflicker.com to get scores by quarter and current game time.
    """
    weekly_scores = []
    current_week = get_nfl_week_num()
    for week in list(range(1, current_week + 1)):
        url = 'http://www.fleaflicker.com/nfl/scores?week={}'.format(week)
        tables = get_xml(url)
        weekly_scores.append(get_weekly_scores(tables, week))

    return pd.concat(weekly_scores).dropna()


def main():

    yearly_scores_df = build_yearly_scores()
    yearly_scores_df.to_csv('tmp/nfl_scores.csv', index=False)


if __name__ == '__main__':
    main()
