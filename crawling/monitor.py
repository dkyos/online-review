#!/usr/bin/env python

import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
#from dateutil.relativedelta import relativedelta
from datetime import date
#from flatten_json import flatten
from tqdm import tnrange as trange
from time import sleep

class CrimsonHexagonClient(object):
    """Interacts with the Crimson Hexagon API to retrieve post data (twitter ids
    etc.) from a configured monitor.

    Docs:
        https://apidocs.crimsonhexagon.com/v1.0/reference

     Args:
        username (str): Username on website.
        password (str): Password on website.
        monitor_id (str): id of crimson monitor.
    """

    def __init__(self, username, password, monitor_id):
        self.username = username
        self.password = password
        self.monitor_id = monitor_id
        self.base = 'https://api.crimsonhexagon.com/api/monitor'
        self.session = requests.Session()
        self.ratelimit_refresh = 60
        self._auth()

    def _auth(self):
        """Authenticates a user using their username and password through the
        authenticate endpoint.
        """
        #url = 'https://forsight.crimsonhexagon.com/api/authenticate?'
        url = "https://api.crimsonhexagon.com/api/authenticate"


        payload = {
            'username': self.username,
            'password': self.password
        }

        r = self.session.get(url, params=payload)
        #j_result = r.json()
        print(r.text)
        j_result = json.loads(r.text)
        self.auth_token = j_result['auth']
        print('-- Authenticated --')
        return

    def make_endpoint(self, endpoint):
        return '{}/{}?'.format(self.base, endpoint)

    def get_data_from_endpoint(self, from_, to_, endpoint):
        """Hits the designated endpoint (volume/posts) for a specified time period.
        The ratelimit is burned through ASAP and then backed off for one minute.
        """
        endpoint = self.make_endpoint(endpoint)
        from_, to_ = str(from_), str(to_)
        payload = {
            'auth': self.auth_token,
            'id': self.monitor_id,
            'start': from_,
            'end': to_,
            'extendLimit': 'true',
            'fullContents': 'true'
        }

        r = self.session.get(endpoint, params=payload)
        self.last_response = r

        ratelimit_remaining = r.headers['X-RateLimit-Remaining']

        # If the header is empty or 0 then wait for a ratelimit refresh.
        if (not ratelimit_remaining) or (float(ratelimit_remaining) < 1):
            print('Waiting for ratelimit refresh...')
            sleep(self.ratelimit_refresh)

        return r

    def get_dates_from_timespan(self, r_volume, max_documents=10000):
        """Divides the time period into chunks of less than 10k where possible.
        """
        # If the count is less than max, just return the original time span.
        if r_volume.json()['numberOfDocuments'] <= max_documents:
            l_dates = [[pd.to_datetime(r_volume.json()['startDate']).date(),
                       pd.to_datetime(r_volume.json()['endDate']).date()]]
            return l_dates

        # Convert json to df for easier subsetting & to calculate cumulative sum.
        df = pd.DataFrame(r_volume.json()['volume'])
        df['startDate'] = pd.to_datetime(df['startDate'])
        df['endDate'] = pd.to_datetime(df['endDate'])

        l_dates = []

        while True:
            df['cumulative_sum'] = df['numberOfDocuments'].cumsum()

            # Find the span whose cumulative sum is below the threshold.
            df_below = df[df['cumulative_sum'] <= max_documents]

            # If there are 0 rows under threshold.
            if (df_below.empty):
                # If there are still rows left, use the first row.
                if len(df) > 0:
                    # This entry will have over 10k, but we can't go more
                    # granular than one day.
                    df_below = df.iloc[0:1]
                else:
                    break

            # Take the first row's start date and last row's end date.
            from_ = df_below['startDate'].iloc[0].date()
            to_ = df_below['endDate'].iloc[-1].date()

            l_dates.append([from_, to_])

            # Reassign df to remaining portion.
            df = df[df['startDate'] >= to_]

        return l_dates

    def plot_volume(self, r_volume):
        """Plots a time-series chart with two axes to show the daily and cumulative
        document count.
        """
        # Convert r to df, fix datetime, add cumulative sum.
        df_volume = pd.DataFrame(r_volume.json()['volume'])
        df_volume['startDate'] = pd.to_datetime(df_volume['startDate'])
        df_volume['endDate'] = pd.to_datetime(df_volume['endDate'])
        df_volume['cumulative_sum'] = df_volume['numberOfDocuments'].cumsum()

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        df_volume['numberOfDocuments'].plot(ax=ax1, style='b-')
        df_volume['cumulative_sum'].plot(ax=ax2, style='r-')

        ax1.set_ylabel('Number of Documents')
        ax2.set_ylabel('Cumulative Sum')

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc=2)

        plt.show()

        return

    '''
    def make_data_pipeline(self, from_, to_):
        """Combines the functionsin this class to make a robust pipeline, that 
        loops through each day in a time period. Data is returned as a dataframe.
        """

        # Get the volume over time data.
        r_volume = self.get_data_from_endpoint(from_, to_, 'volume')
        print('There are approximately {} documents.'.format(r_volume.json()['numberOfDocuments']))
        self.plot_volume(r_volume)

        # Carve up time into buckets of volume <10k.
        l_dates = self.get_dates_from_timespan(r_volume)

        data = []

        for i in trange(len(l_dates), leave=False):
            from_, to_ = l_dates[i]

            # Pull posts.
            r_posts = self.get_data_from_endpoint(from_, to_, 'posts')
            if r_posts.ok and (r_posts.json()['status'] != 'error'):
                j_result = json.loads(r_posts.content.decode('utf8'))
                data.extend(j_result['posts'])

        l_flat= [flatten(d) for d in data]
        df = pd.DataFrame(l_flat)

        return df
    '''

if __name__ == "__main__":

    # Credentials.
    username = 'xxx'
    password = 'yyy'


    # Monitor id - taken from URL on website.
    monitor_id = '1234'

    # Instantiate client.
    crimson_api = CrimsonHexagonClient(username, password, monitor_id)

    #from_ = date(2017, 1, 1)
    #to_   = date(2017, 6, 30)

    # Combine class functions into a typical workflow.
    #df = crimson_api.make_data_pipeline(from_, to_)
