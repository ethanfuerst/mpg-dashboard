import pandas as pd
import numpy as np
import datetime as dt
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import urllib.request, json, time, sys
import json
# import environ


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
    
    # env = environ.Env(
    #     # set casting, default value
    #     DEBUG=(bool, False)
    # )

    creds_dict = {
        "type": "service_account",
        "project_id": os.environ["project_id"],
        "private_key_id": os.environ["private_key_id"],
        "private_key": os.environ["private_key"].replace("\\n", "\n"),
        "client_email": os.environ["client_email"],
        "client_id": os.environ["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ["client_x509_cert_url"]
    }

    with open('api_creds.json', 'w') as fp:
        json.dump(creds_dict, fp)

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('api_creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('MPG Data')
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    df = pd.DataFrame.from_dict(records_data)

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
