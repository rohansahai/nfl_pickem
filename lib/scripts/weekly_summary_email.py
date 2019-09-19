import pandas as pd
from util import send_html_email, get_nfl_week_num, EmailBody
from db import get_prod_str
import seaborn as sns


def get_weekly_picks(outcome_cols, prod_str):
    """
    :return:
    """
    picks_q = """
    SELECT
    
        u.name as user,
        p.game_id,
        t.name as team,
        p.week,
        p.result
        
    from picks p

    LEFT JOIN users u on p.user_id = u.id

    LEFT JOIN teams t on p.winner_id = t.id
    
    where p.league_id = 1"""

    picks_df = pd.read_sql(picks_q, prod_str)
    for col in outcome_cols:
        picks_df[col] = picks_df['result'].apply(lambda result: 1 if result == col else 0)
        picks_df['weekly_{}'.format(col)] = picks_df.groupby('week')[col].transform(sum)
        picks_df['user_{}'.format(col)] = picks_df.groupby(['user', 'week'])[col].transform(sum)

    return picks_df


def get_weekly_league_record(picks_df, outcome_cols, week):
    """
    :param picks_df:
    :return:
    """
    weekly_league_record = picks_df[['week'] + ['weekly_{}'.format(col) for col in outcome_cols]].drop_duplicates()
    weekly_league_record['weekly_points'] = weekly_league_record['weekly_win'] + (
    weekly_league_record['weekly_push'] * .5)
    weekly_league_record['win_rate'] = weekly_league_record['weekly_points'] / \
                                       (weekly_league_record['weekly_win'] + weekly_league_record['weekly_loss'] +
                                        weekly_league_record['weekly_push']) * 100
    weekly_league_record['win_rate'] = weekly_league_record['win_rate'].apply(lambda x: '{:.1f}'.format(x))
    weekly_league_record.sort_values('week', inplace=True)
    weekly_league_record.columns = ['Week', 'Wins', 'Loss', 'Push', 'Points', 'Win Rate (%)']
    weekly_league_record = weekly_league_record[weekly_league_record['Week'] <= week]
    weekly_league_record['Win Rate (%)'] = weekly_league_record['Win Rate (%)'].astype(float)

    sns.set(style="darkgrid")
    ax = sns.lineplot(x="Week", y="Win Rate (%)", data=weekly_league_record)
    ax.figure.savefig('/Users/shaunchaudhary/Desktop/Weekly League Batting Average.png')
    ax.figure.clf()

    return weekly_league_record


def get_weekly_ind_record(picks_df, outcome_cols, week):
    """
    :param picks_df:
    :param outcome_cols:
    :param week:
    :return:
    """
    weekly_ind_record = picks_df[['user', 'week'] + ['user_{}'.format(col) for col in outcome_cols]].drop_duplicates()
    rec_format = lambda row: '{}-{}-{}'.format(row['user_win'], row['user_loss'], row['user_push'])
    weekly_ind_record['weekly_record'] = weekly_ind_record.apply(rec_format, axis=1)
    weekly_ind_record['weekly_points'] = weekly_ind_record['user_win'] + (weekly_ind_record['user_push'] * .5)
    weekly_ind_record = weekly_ind_record[['user', 'week', 'weekly_record', 'weekly_points']]
    weekly_ind_record['record_count'] = weekly_ind_record.groupby(['weekly_record', 'week'])['user'].transform('count')
    weekly_ind_record = weekly_ind_record[weekly_ind_record['week'] == week].sort_values('weekly_points', ascending=False)

    return weekly_ind_record


def get_current_week_rec_dis(weekly_ind_record, week):
    """
    :param weekly_ind_record:
    :param week:
    :return:
    """
    current_week_rec_dist = weekly_ind_record[
        ['week', 'weekly_record', 'record_count', 'weekly_points']].drop_duplicates().sort_values('weekly_points',
                                                                                                  ascending=False)
    current_week_rec_dist = current_week_rec_dist[current_week_rec_dist['week'] == week]
    current_week_rec_dist.drop('week', axis=1, inplace=True)
    current_week_rec_dist.columns = ['Record', 'Count', 'Points']

    e = sns.barplot(x="Record", y="Count", data=current_week_rec_dist, dodge=False)
    e.figure.savefig('/Users/shaunchaudhary/Desktop/Weekly Record Distribution.png')
    e.figure.clf()


def build_weekly_email(weekly_league_record):
    """
    :param weekly_league_record:
    :return:
    """
    intro = """Hello!\n
    We have 5 5-0s this week so each person will receive $30 dollars via venmo.\n

    Updated <a href="https://www.superpickem.me/standings">standings</a> are available on the website.\n
    Let me know if you have any questions."""

    picks_email = EmailBody(msg=intro)
    picks_email.add_df_html(weekly_league_record, msg='League Record', underline=True, bold=True, index=False)
    # picks_email.add_df_html(weekly_ind_record, msg='Individual Records', underline=True, bold=True, index=False)
    # picks_email.add_df_html(current_week_rec_dist, msg='Record Distributions', underline=True, bold=True, index=False)

    outro = """
    Also, <a href="https://www.superpickem.me/picks">Week 3 spreads</a> are up!\n
    Best,
    Shaun"""

    picks_email.add_msg(msg=outro)

    return picks_email


def main():

    prod_str = get_prod_str()
    week = get_nfl_week_num()
    outcome_cols = ['win', 'loss', 'push']
    picks_df = get_weekly_picks(outcome_cols, prod_str)
    weekly_league_record = get_weekly_league_record(picks_df, outcome_cols, week)
    weekly_ind_record = get_weekly_ind_record(picks_df, outcome_cols, week)
    get_current_week_rec_dis(weekly_ind_record, week)
    picks_email = build_weekly_email(weekly_league_record)

    send_html_email(picks_email.html, 'Week {0} Results and Week {1} Spreads'.format(week-1, week),
                    'shaun.chaudhary@gmail.com', 'shaun.chaudhary@gmail.com')


# if __name__ == '__main__':
#     main()
