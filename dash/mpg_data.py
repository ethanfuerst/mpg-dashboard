import pandas as pd
import numpy as np
import datetime as dt
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import urllib.request, json, time, sys


def money_format(x):
    return '${:.2f}'.format(x)

def lin_reg(X, Y):
    lr = LinearRegression()
    lr.fit(X.values.reshape(-1, 1),Y)
    intercept = lr.intercept_
    slope = lr.coef_[0]
    preds = slope * X + intercept
    rmse = round(np.sqrt(metrics.mean_squared_error(Y, preds)), 3)
    r_2 = round(metrics.r2_score(Y, preds), 2)
    return slope, intercept, preds, rmse, r_2

def get_data():
    '''
    Pulls mpg data from https://docs.google.com/spreadsheets/d/1bTuNfyXJwygTJ8pQlo7PzdxfymQ_lB7DBzFoWHxJxkk
    and returns a formatted df
    '''
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

    sheets = service.spreadsheets()

    result = sheets.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    values = result.get('values', [])

    df = pd.DataFrame(columns=values[0], data=values[1:])
    df = df.replace(r'^\s*$', np.nan, regex=True).copy()
    df = df.dropna().copy()

    df['miles'] = round(df['miles'].astype(float), 1)
    df['dollars'] = round(df['dollars'].astype(float), 2)
    df['gallons'] = round(df['gallons'].astype(float), 3)

    df['gal_cost'] = round(df['dollars'] / df['gallons'], 2)
    df['mpg'] = round(df['miles'] / df['gallons'], 2)

    # - 2017 Jeep Patriot tank size = 13.55 gallons
    df['tank%_used'] = round(df['gallons'] / 13.55, 4)

    df['date'] = pd.to_datetime(df['date'].astype(str))
    df['weekday'] = df['date'].dt.dayofweek.apply(lambda x: ['Monday', 'Tuesday', 'Wednesday', 
                                                    'Thursday', 'Friday', 'Saturday', 'Sunday'][x])
    df['days_since_last_fillup'] = df['date'].diff().dt.days
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%m/%d/%y')

    df['dollars per mile'] = round(df['dollars'] / df['miles'], 4)
    df['miles per day'] = round(df['miles'] / df['days_since_last_fillup'], 2)
    
    return df

def insight_creator(df):
    '''
    When passed a df after going through get_data,
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

    time_periods = {'Last Fillup':last_fillup, 'Last Month':last_month, 'Last 3 Months':last_3, 
                    'Last 6 Months':last_6, 'Last Year':last_year, 'All Time':all_time}

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
