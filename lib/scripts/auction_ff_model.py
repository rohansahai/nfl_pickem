import pandas as pd

file_path = '/Users/shaunchaudhary/Desktop/2018_19_auction_ff.csv'
players_df = pd.read_csv(file_path)

total = 200
starting_lineup = 180

cur_lineup = {
    'QB': '',
    'RB1': '',
    'RB2': '',
    'WR1': '',
    'WR2': '',
    'TE': ''}

lineup = []
for name, group in players_df.groupby('Position'):
    group.sort_values('Auction_Val', ascending=False)
    if name in ('QB', 'TE'):
        lineup.append(group.iloc[0].tolist())
    else:
        for i in range(2):
            lineup.append(group.iloc[i].tolist())

final_lineup = pd.DataFrame(lineup, columns=players_df.columns)

final_lineup['seq'] = 0
final_lineup['Money_Spent'] = final_lineup['Auction_Val'].sum()
final_lineup['Rank_Sum'] = final_lineup['Rank'].sum()

