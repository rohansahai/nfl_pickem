import pandas as pd


def build_user_id_mapping():
    """
    returns: use manual ordered list to return dictionary of user: user id
    """
    users = [
        'Rohan Sahai',
        'Shaun Chaudhary',
        'Joseph Della Fera',
        'Ryan John',
        'Brandon Sarna',
        'Michael Stone',
        'Bryan Ashley',
        'James Detmer',
        'Joseph Iantosca',
        'Alex Miller',
        'AJ LeGaye',
        'David Kafafian',
        'Matthew Rosen',
        'Dylan Levy',
        'Joseph Peters',
        'Neal Dennison',
        'Chris Kreider',
        "Will O'Leary",
        'Varun Deedwaniya',
        'James Heine',
        'Brett Graffy',
        'Karan Bathija',
        'Shawn Israilov',
        'Alex Burness',
        'Will Perge']

    return {user: i+1 for i, user in enumerate(users)}


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


def build_existing_picks_df(existing_picks_file):
    """
    returns: build user id and team id mapping. Read in historical picks and convert string cols to ids.
    """
    user_id_mapping = build_user_id_mapping()
    team_id_mapping = build_team_id_mapping()

    existing_picks_df = pd.read_excel(existing_picks_file, sheetname='existing picks_string')

    existing_picks_df['user_id'] = existing_picks_df['user_id'].map(user_id_mapping)
    for col in ['team_id', 'ml_winner_id', 'spread_winner_id']:
        existing_picks_df[col] = existing_picks_df[col].map(team_id_mapping)

    return existing_picks_df


def main():

    existing_picks_file = input("Enter directory of existing picks data: ")
    file_out = input("Enter destination for existing picks with ids: ")
    existing_picks_df = build_existing_picks_df(existing_picks_file)
    existing_picks_df.to_csv(file_out, index=False)


if __name__ == '__main__':
    main()