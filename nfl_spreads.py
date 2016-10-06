import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from dateutil import parser
from datetime import datetime as dt
import numpy as np


def get_pinnacle_xml():

    url = urlopen("http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Football&sportsubtype=nfl")
    data = url.read()
    url.close()

    return BeautifulSoup(data, 'lxml')


def create_week_mapping_df():

    week_begin = pd.date_range(start='2016-09-13', end='2016-12-27', freq='7D')
    week_end = pd.date_range(start='2016-09-19', end='2017-01-02', freq='7D')
    week_nums = list(range(2, 18))
    week_lol = [[dt(2016, 8, 1), dt(2016, 9, 12), 1]] + [[week_b, week_e, num] for week_b, week_e, num in
                                                         zip(week_begin, week_end, week_nums)]

    return pd.DataFrame(week_lol, columns=['Week_Begin', 'Week_End', 'Week_Num'])


def parse_pinnacle_xml(nfl_data, week_mapping_df):

    today = dt.today()
    nfl_sched = []
    for event in nfl_data.find_all('event'):
        gmt_gametime = parser.parse(event.event_datetimegmt.extract().string.extract())
        visiting, home = [team.string.extract() for team in event.find_all('participant_name')]
        try:
            visiting_spread = event.spread_visiting.extract().string.extract()
        except AttributeError:
            visiting_spread = np.nan
        try:
            home_spread = event.spread_home.extract().string.extract()
        except AttributeError:
            home_spread = np.nan
        nfl_sched.append([gmt_gametime, visiting, float(visiting_spread), home, float(home_spread)])

    cols = ['GMT_Game Time', 'Visiting Team', 'Visiting Spread', 'Home Team', 'Home Spread']

    nfl_sched_df = pd.DataFrame(nfl_sched, columns=cols)
    nfl_sched_df['GMT_Game Time'] = nfl_sched_df['GMT_Game Time'].dt.tz_localize('GMT')
    nfl_sched_df['EST_Game Time'] = nfl_sched_df['GMT_Game Time'].dt.tz_convert('US/Eastern')
    nfl_sched_df['EST_Game Time'] = pd.to_datetime(nfl_sched_df['EST_Game Time'])
    nfl_sched_df['Week_Num'] = week_mapping_df.loc[(week_mapping_df['Week_Begin'] <= today) &
                                                   (week_mapping_df['Week_End'] >= today)]['Week_Num'].iloc[0]

    return nfl_sched_df.drop('GMT_Game Time', axis=1)


def main():

    nfl_data = get_pinnacle_xml()
    week_mapping_df = create_week_mapping_df()
    nfl_sched_df = parse_pinnacle_xml(nfl_data, week_mapping_df)[:-1]


