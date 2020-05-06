#%%
import pandas as pd
import datetime as dt
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import urllib.request, json, os, itertools, threading, time, sys

# This is used for computing the moving average with the weather data
window = 5

#%%
if __name__ == '__main__':
    print("Please do not close the window.")
    print("mpg_refresh.py will print how long it took to run when it is completed.")
    done = False
    # a nice animation while the program is running
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rmpg_refresh.py is running ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\n')

    t = threading.Thread(target=animate)
    t.start()

# lets see how long this takes
startTime = datetime.now()

#%%
'''
First I will pull the data from car_mpg_data.csv, create new columns
and save it back to car_mpg_data.csv
'''

df = pd.read_csv('car_mpg_data.csv')
df.name = 'Car Data'

def mpg_data_creator(df):
    '''
    When passed a df with these columns:
    miles, dollars, gallons, date
    this method will return a df with the following columns:
    gal_cost, mpg, tank%_used, weekday, days_since_last_fillup, dollars per mile
    '''
    df = df[['miles', 'dollars', 'gallons', 'date']].copy()
    df['miles'] = df['miles'].astype(float)
    df['dollars'] = df['dollars'].astype(float)
    df['gallons'] = df['gallons'].astype(float)

    # creating gal_cost and mpg
    df['gal_cost'] = df['dollars'] / df['gallons']
    df['mpg'] = df['miles'] / df['gallons']

    # creating a new column to determine what percent of my tank was used up when filled up
    # car tank size = 13.55 gallons
    df['tank%_used'] = df['gallons'] / 13.55

    # following method used in for loop
    def as_day(i):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[i]

    # changes column to datetime
    df['date'] = pd.to_datetime(df['date'].astype(str))

    # creates column with day of the week
    df['weekday'] = df['date'].dt.dayofweek
    df['weekday'] = df['weekday'].apply(as_day)

    # creates a new column that records the number of days since the last fillup
    df['days_since_last_fillup'] = df['date'].diff().dt.days

    # add column for cost to go one mile
    df['dollars per mile'] = df['dollars'] / df['miles']

    return df

df = mpg_data_creator(df)
df.name = 'Car data'

# save back to car_mpg_data.csv
df.to_csv('car_mpg_data.csv', index=False)

#%%
'''
Create a .csv for a dashboard of insights
'''

last_fillup = df.tail(1).copy()
last_month = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=1))].copy()
last_3 = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=3))].copy()
last_6 = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(months=6))].copy()
last_year = df[df['date'] >= pd.Timestamp(date.today() - relativedelta(years=1))].copy()
all_time = df.copy()

time_periods = {'Last Fillup':last_fillup, 'Last Month':last_month, 'Last 3 Months':last_3, 'Last 6 Months':last_6, 'Last Year':last_year, 'All Time':all_time}

insights = []
labels = ['Time period', 'Miles', 'Dollars', 'Gallons', 'MPG', 'Avg gallon cost', 'Cost to go one mile']
for key, value in time_periods.items():
    insight_row = [key, sum(value['miles']), sum(value['dollars']), sum(value['gallons'])]
    insight_row.append(sum(value['miles']) / sum(value['gallons']))
    insight_row.append(sum(value['dollars']) / sum(value['gallons']))
    insight_row.append(sum(value['dollars']) / sum(value['miles']))
    insights.append(insight_row)
    insight_row = []

df_insights = pd.DataFrame(insights, columns=labels)
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
    print("Cost to go one mile: $" + str(round(sum(df['dollars'])/sum(df['miles']), 2)))

#%%
if __name__ == '__main__':
    # stop the animation and print the time
    minutes, seconds = divmod((datetime.now() - startTime).seconds,60)
    print("mpg_refresh.py ran in {} minutes and {} seconds".format(minutes,seconds))

    done = True
    mpg_insights(df)

# %%
