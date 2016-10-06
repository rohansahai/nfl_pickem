import pandas as pd

folder = '/Users/shaunchaudhary/documents/personal/nfl_pick_em/'
team_id_df = pd.read_csv(folder + 'team_id_mapping.csv')
team_id_df.rename(columns={'team_name': 'Team'}, inplace=True)
weekly_games_df = pd.read_csv(folder + 'weekly_games.csv')

weekly_games_df = pd.merge(weekly_games_df, team_id_df, how='left', left_on='home_team_id', right_on='Team')
weekly_games_df.drop(['home_team_id', 'Team'], axis=1, inplace=True)
weekly_games_df.rename(columns={'id': 'home_team_id'}, inplace=True)
weekly_games_df = pd.merge(weekly_games_df, team_id_df, how='left', left_on='away_team_id', right_on='Team')
weekly_games_df.drop(['away_team_id', 'Team'], axis=1, inplace=True)
weekly_games_df.rename(columns={'id': 'away_team_id'}, inplace=True)

weekly_games_df = weekly_games_df[['week', 'home_team_id', 'away_team_id', 'home_spread',
                                   'time', 'created_at', 'updated_at']]

for col in ['time', 'created_at', 'updated_at']:
    weekly_games_df[col] = pd.to_datetime(weekly_games_df[col])