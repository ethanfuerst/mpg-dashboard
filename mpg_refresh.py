#%%
import pandas as pd
import datetime as dt
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import urllib.request, json, os, itertools, threading, time, sys

#%%
def get_data():
# from https://developers.google.com/sheets/api/quickstart/python
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = '1bTuNfyXJwygTJ8pQlo7PzdxfymQ_lB7DBzFoWHxJxkk'
    range_name = 'Data!A:D'
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scope)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])

    df = pd.DataFrame(columns=values[0], data=values[1:])

    df = create_data(df)

    return df

#%%
def create_data(df):
    '''
    When passed a df with these columns:
    miles, dollars, gallons, date
    this method will return a df with the following columns:
    gal_cost, mpg, tank%_used, weekday, days_since_last_fillup, dollars per mile, miles per day
    '''
    df['miles'] = round(df['miles'].astype(float), 1)
    df['dollars'] = round(df['dollars'].astype(float), 2)
    df['gallons'] = round(df['gallons'].astype(float), 3)

    # - creating gal_cost and mpg
    df['gal_cost'] = round(df['dollars'] / df['gallons'], 2)
    df['mpg'] = round(df['miles'] / df['gallons'], 2)

    # - creating a new column to determine what percent of my tank was used up when filled up
    # - 2017 Jeep Patriot tank size = 13.55 gallons
    df['tank%_used'] = round(df['gallons'] / 13.55, 4)

    # - changes column to datetime
    df['date'] = pd.to_datetime(df['date'].astype(str))

    # - creates column with day of the week
    df['weekday'] = df['date'].dt.dayofweek.apply(lambda x: ['Monday', 'Tuesday', 'Wednesday', 
                                                    'Thursday', 'Friday', 'Saturday', 'Sunday'][x])

    # - creates a new column that records the number of days since the last fillup
    df['days_since_last_fillup'] = df['date'].diff().dt.days

    # - change back to string format
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d/%y')

    # - add column for cost to go one mile
    df['dollars per mile'] = round(df['dollars'] / df['miles'], 4)

    # - new column for avg miles per day
    df['miles per day'] = round(df['miles'] / df['days_since_last_fillup'], 2)

    return df

#%%

df = get_data()

#%%

# - Create a .csv for a dashboard of insights
def insight_creator(df):
    '''
    When passed a df after going through get_data or create_data,
    this method will return a df that will provide insights on the data in different time frames
    '''
    df = df.fillna(0).copy()
    df['date'] = pd.to_datetime(df['date'].astype(str))
    last_fillup = df.tail(1).copy()
    last_month = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=1))].copy()
    last_3 = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=3))].copy()
    last_6 = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=6))].copy()
    last_year = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(years=1))].copy()
    all_time = df.copy()

    time_periods = {'Last Fillup':last_fillup, 'Last Month':last_month, 'Last 3 Months':last_3, 'Last 6 Months':last_6, 'Last Year':last_year, 'All Time':all_time}

    df_insights = pd.DataFrame(columns=['Time period', 'Miles', 'Dollars', 'Gallons', 
                                        'MPG', 'Avg gallon cost', 'Cost to go one mile (in cents)',
                                        'Average miles per day'])

    for i in range(len(time_periods)):
        value = list(time_periods.values())[i]
        df_insights.loc[i] = [list(time_periods.keys())[i], 
                                round(sum(value['miles']),3), 
                                round(sum(value['dollars']),3), 
                                round(sum(value['gallons']),3), 
                                round(sum(value['miles']) / sum(value['gallons']),3), 
                                round(sum(value['dollars']) / sum(value['gallons']),2), 
                                round(sum(value['dollars']) / sum(value['miles']) * 100 ,1),
                                round(sum(value['miles']) / sum(value['days_since_last_fillup']),2)]
    
    return df_insights

df_insights = insight_creator(df)
# %%
# - lastly, just run the mpg_vis file to update all the visualizations
import mpg_vis