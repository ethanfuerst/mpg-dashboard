#%%
import pandas as pd
import datetime as dt
from datetime import date, timedelta, datetime
import urllib.request, json, os, itertools, threading, time, sys

# This is used for computing the moving average with the weather data
window = 5

#%%
print("Please do not close the window.")
print("mpg_extract.py will print how long it took to run when it is completed.")
done = False
# a nice animation while the program is running
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rmpg_extract.py is running ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\n')

t = threading.Thread(target=animate)
t.start()

# lets see how long this takes
startTime = datetime.now()

#%%
'''
First I will pull the data from moped_mpg_data.csv and car_mpg_data.csv
and save them as clean_c_data.csv and clean_m_date.csv
'''

df_m = pd.read_csv('moped_mpg_data.csv')
df_m.name = 'Moped Data'
df_c = pd.read_csv('car_mpg_data.csv')
df_c.name = 'Car Data'

# creating new column for how much a gallon of gas cost for each entry
for i in [df_m, df_c]:
    i['gal_cost'] = i.dollars / i.gallons
    i['mpg'] = i.miles / i.gallons

# creating a new column to determine what percent of my tank was used up when filled up
# moped tank size = 1.37 gallons
df_m['tank%_used'] = df_m['gallons'] / 1.37
# car tank size = 13.55 gallons
df_c['tank%_used'] = df_c['gallons'] / 13.55

# following method used in for loop
def as_day(i):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[i]

for i in [df_m, df_c]:
    # changes column to datetime
    i['date'] = pd.to_datetime(i['date'])

    # creates column with day of the week
    i['day'] = i['date'].dt.dayofweek
    i['day'] = i['day'].apply(as_day)

    # creates a new column that records the number of days since the last fillup
    i['days_since_last_fillup'] = i['date'].diff().dt.days

# creates unique id in the form vehicle-date-index of vechicle df
df_c = df_c.assign(id=('c' + '-' + df_c['date'].dt.strftime("%d-%b-%Y") + "-" + df_c.index.map(str)))
df_m = df_m.assign(id=('m' + '-' + df_m['date'].dt.strftime("%d-%b-%Y") + "-" + df_m.index.map(str)))

# creates clean_c_data.csv and clean_m_data.csv
df_c.to_csv('clean_c_data.csv')
df_m.to_csv('clean_m_data.csv')
#%%
'''
Now to get the weather data from https://darksky.net/
'''

# https://darksky.net/dev/docs requests I keep my key hidden
# Going back a directory to access darkskyid.txt and save as my_id
os.chdir("..")
id = open('darkskyid.txt', 'r').read()
# Going back to original directory
os.chdir("/Users/ethanfuerst/Documents/Coding/mpgdata")

def get_weather(lat, long, id, sdate, window=1, edate=date.today()):
    '''
    This method returns a dataframe that contains the high temp, low temp, moving average high and moving average low for a range of days.
    The dataframe returned will contain all data from the startdate through the day before the enddate.

    Parameters:


    lat (float, required)
        The latitude of where you want data from

    long (float, required)
        The longitude of where you want data from

    id (string, required)
        The ID for darksky API.
        For more info, visit https://darksky.net/
        
    sdate (datetime.date, required)
        The startdate of the interval
        Must be a datetime.date object
    
    window (optional, default is 1)
        The moving window for the moving average column
    
    edate (optional, default is date.today())
        The enddate of the interval
        Must be a datetime.date object
    '''
    # creating a list for each day in the range
    # using unix time because that's what the darksky api uses
    # each date will give me the unix time at 6pm for that day
    # the daily_high and daily_low are the parameters that I will use to see how my mpg changes
    delta = edate - sdate       # as timedelta
    date_list = []
    for i in range(window * -1, delta.days + 1):
        day = sdate + timedelta(days=i)
        date_list.append(int((day - dt.date(1970,1,1)).total_seconds()))

    # creating a list for each api call
    api_list = []
    for i in date_list:
        api_list.append('https://api.darksky.net/forecast/'+str(id)+'/'+str(lat)+','+str(long)+','+str(i)+'?exclude=flags,hourly')

    # getting the high temp and low temp for each day
    dates = []
    daily_high = []
    daily_low = []
    for api in api_list:
        with urllib.request.urlopen(api) as url:
            data = json.loads(url.read().decode())
            # keeping day in yyyymmdd format, just like in other dataframes
            dates.append(datetime.fromtimestamp(data["currently"]["time"]).strftime("20%y/%m/%d"))
            daily_high.append(data["daily"]["data"][0]["temperatureHigh"])
            daily_low.append(data["daily"]["data"][0]["temperatureLow"])

    # putting all the lists in to a dateframe
    df_weather = pd.DataFrame({'date': dates, 'daily_high': daily_high, 'daily_low': daily_low})
    if window != 1:
        df_weather['high_mov_avg'] = df_weather['daily_high'].rolling(window=window).mean()
        df_weather['low_mov_avg'] = df_weather['daily_low'].rolling(window=window).mean()

    # need to drop the records before the sdate
    drop_list = [i for i in range(window+1)]
    df_weather = df_weather.drop(drop_list)
    # and then reset the index
    df_weather.reset_index(drop=True, inplace=True)

    return df_weather

old_df = pd.read_csv('weather_data.csv')
old_df.drop('Unnamed: 0', axis=1, inplace=True)

# Get top temp with current window
sdate = date(2018, 12, 31 - (window - 2))
edate = date(2019, 1, 2)
test_df = get_weather(sdate=sdate, lat=30.267153, long=-97.7430608, id=id, window=window, edate=edate)
f_temp = test_df['low_mov_avg'].iloc[-1].round(3)

# If the last date in the df is the same as the yesterday then we are good to go
date_array = old_df['date'].iloc[-1].split('/')
old_df_today = date(int(date_array[0]), int(date_array[1]), int(date_array[2]))
# If the top temp (jan 1) from the small df is the same as the old df
# and todays date is the same as the most recent date on the old df
# then we set df_weather to old_df. Nothing changed.
if (f_temp == old_df['low_mov_avg'].iloc[0].round(3)) and (old_df_today == (date.today() - timedelta(1))):
    df_weather = old_df
# If the top temp is different, i.e. the moving average changed, we have to recompute everything
elif  f_temp != old_df['low_mov_avg'].iloc[0].round(3):
    # creating a range of dates to get - shoutout date.today()
    # I'm using a moving average that changes, so doing this I will have data Jan 1 2019
    # window is defined around line 8
    df_weather = get_weather(sdate=date(2019, 1, 1), lat=30.267153, long=-97.7430608, id=id, window=window)
# Lastly, if the top temp is the same then we can just add the days that we have been missing
else:
    l_date = old_df['date'].iloc[-1].split('/')
    sdate = date(int(l_date[0]), int(l_date[1]), int(l_date[2])) + timedelta(1)   # last date + one day
    new_days = get_weather(sdate=sdate, lat=30.267153, long=-97.7430608, id=id, window=window)
    df_weather = pd.concat([old_df, new_days], sort=False)

# Need to figure out when to use this
# df_weather.drop([i for i in range(0, window - 1)], inplace=True)

#%%
# and finally ... saving the df_weather to a .csv
df_weather.reset_index(drop=True, inplace=True)
df_weather = df_weather[['date', 'daily_high', 'daily_low', 'high_mov_avg', 'low_mov_avg']]
df_weather.to_csv('weather_data.csv')

# stop the animation and print the time
minutes, seconds = divmod((datetime.now() - startTime).seconds,60)
print("mpg_extract.py ran in {} minutes and {} seconds".format(minutes,seconds))

done = True

# %%