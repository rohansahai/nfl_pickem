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
    games = [tds[i:i + 8] for i in range(0, len(tds), 8)]
    scores = []
    for xml in games:
        ind_game_data = []
        away_home = [xml[i:i + 3] for i in range(0, len(xml), 3)]
        for i, game in enumerate(away_home[:-1]):
            try:
                team = game[0].img['alt']
                score = int([score.strip() for score in game[1]][0])
                if i == 0:
                    ind_game_data.extend([team, score])
                else:
                    ind_game_data.extend([team, score, away_home[2][0].img['alt']])
            except (ValueError, TypeError):
                ind_game_data = []

        scores.append(ind_game_data)

    return scores


def get_ml_winner(row):
    """
    returns: Identify winner of each game.
    """
    if row['home_score'] > row['away_score']:
        return row['home_team_id']
    else:
        return row['away_team_id']


def build_team_id_mapping():
    """
    returns: Map sorted teams (descending) to id.
    """
    teams = [
        'Arizona Cardinals',
        'Atlanta Falcons',
        'Baltimore Ravens',
        'Buffalo Bills',
        'Carolina Panthers',
        'Chicago Bears',
        'Cincinnati Bengals',
        'Cleveland Browns',
        'Dallas Cowboys',
        'Denver Broncos',
        'Detroit Lions',
        'Green Bay Packers',
        'Houston Texans',
        'Indianapolis Colts',
        'Jacksonville Jaguars',
        'Kansas City Chiefs',
        'Los Angeles Rams',
        'Miami Dolphins',
        'Minnesota Vikings',
        'New England Patriots',
        'New Orleans Saints',
        'New York Giants',
        'New York Jets',
        'Oakland Raiders',
        'Philadelphia Eagles',
        'Pittsburgh Steelers',
        'San Diego Chargers',
        'San Francisco 49ers',
        'Seattle Seahawks',
        'Tampa Bay Buccaneers',
        'Tennessee Titans',
        'Washington Redskins']

    return {team: i+1 for i, team in enumerate(teams)}


def get_weekly_scores(tables, week):
    """
    returns: Find all games and build a DataFrame with each game, the scores and the money line
    winner.
    """
    scores = []
    for table in tables[:-1]:
        tds = table.find_all('td')
        scores.extend(create_score_row(tds))

    team_id_mapping = build_team_id_mapping()
    nfl_score_cols = ['away_team_id', 'away_score', 'home_team_id', 'home_score', 'spread_winner']
    nfl_scores_df = pd.DataFrame(scores, columns=nfl_score_cols)
    nfl_scores_df['ml_winner'] = nfl_scores_df.apply(get_ml_winner, axis=1)

    for col in ['away_team_id', 'home_team_id', 'ml_winner']:
        nfl_scores_df[col] = nfl_scores_df[col].map(team_id_mapping)
    nfl_scores_df['week'] = week

    return nfl_scores_df.drop('spread_winner', axis=1)


def build_yearly_scores():

    weekly_scores = []
    current_week = get_nfl_week_num()
    for week in list(range(1, current_week + 1)):
        url = 'https://fantasysupercontest.com/nfl-lines-2016-week-{}'.format(week)
        tables = get_xml(url)
        weekly_scores.append(get_weekly_scores(tables, week))

    return pd.concat(weekly_scores).dropna()


def main():

    yearly_scores_df = build_yearly_scores()
    yearly_scores_df.to_csv('/Users/shaunchaudhary/desktop/nfl_scores', index=False)


if __name__ == '__main__':
    main()
