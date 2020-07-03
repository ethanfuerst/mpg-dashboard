#%%
import pandas as pd
import datetime as dt
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import urllib.request, json, os, itertools, threading, time, sys

#%%

# - First I will pull the data from car_mpg_data.csv, create new columns
# - and save it back to car_mpg_data.csv

df = pd.read_csv('car_mpg_data.csv')

def mpg_data_creator(df):
    '''
    When passed a df with these columns:
    miles, dollars, gallons, date
    this method will return a df with the following columns:
    gal_cost, mpg, tank%_used, weekday, days_since_last_fillup, dollars per mile
    '''
    df = df[['miles', 'dollars', 'gallons', 'date']].copy()
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

    # - add column for cost to go one mile
    df['dollars per mile'] = round(df['dollars'] / df['miles'], 4)

    return df

df = mpg_data_creator(df)

# - save back to car_mpg_data.csv
df.name = '2017 Jeep Patriot Miles Per Gallon Data'
df.to_csv('car_mpg_data.csv', index=False)

#%%

# - Create a .csv for a dashboard of insights
def insight_creator(df):
    '''
    When passed a df after going through mpg_data_creator,
    this method will return a df that will provide insights on the data in different time frames
    '''
    last_fillup = df.tail(1).copy()
    last_month = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=1))].copy()
    last_3 = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=3))].copy()
    last_6 = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=6))].copy()
    last_year = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(years=1))].copy()
    all_time = df.copy()

    time_periods = {'Last Fillup':last_fillup, 'Last Month':last_month, 'Last 3 Months':last_3, 'Last 6 Months':last_6, 'Last Year':last_year, 'All Time':all_time}

    df_insights = pd.DataFrame(columns=['Time period', 'Miles', 'Dollars', 'Gallons', 
                                        'MPG', 'Avg gallon cost', 'Cost to go one mile (in cents)'])

    for i in range(len(time_periods)):
        value = list(time_periods.values())[i]
        df_insights.loc[i] = [list(time_periods.keys())[i], 
                                round(sum(value['miles']),3), 
                                round(sum(value['dollars']),3), 
                                round(sum(value['gallons']),3), 
                                round(sum(value['miles']) / sum(value['gallons']),3), 
                                round(sum(value['dollars']) / sum(value['gallons']),2), 
                                round(sum(value['dollars']) / sum(value['miles']) * 100 ,1)]
    
    return df_insights

df_insights = insight_creator(df)

df_insights.to_csv('mpg_insights.csv', index=False)

#%%
def mpg_insights(df):
    '''
    Print insights
    '''
    print()
    print(df.name + ':')
    print("Total miles: " + str(round(sum(df['miles']), 2)) + " miles")
    print("Total spent on gas: $" + str(round(sum(df['dollars']), 2 )))
    print("Total gallons pumped: " + str(round(sum(df['gallons']), 2)) + " gallons")
    print("Miles per gallon: " + str(round(sum(df['miles'])/sum(df['gallons']), 2)))
    print("Average cost of one gallon of gas: $" + str(round(sum(df['dollars'])/sum(df['gallons']), 2)))
    print("Cost to go one mile: " + str(round(sum(df['dollars'])/sum(df['miles']) * 100, 3)) + " cents")
    print()

#%%
if __name__ == '__main__':
    mpg_insights(df)

# %%
