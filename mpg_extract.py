import pandas as pd
import datetime as dt

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

# I no longer use the file clean_all_data.csv with my tableau workbook
# Instead, I have two separate workbooks that link to the respective .csvs
# I've deleted clean_all_data.csv, but the code below will recreate it

# df_m['vehicle'] = 'Moped'
# df_c['vehicle'] = 'Car'

# # creates and saves clean_all_data.csv
# all_data = pd.concat([df_m, df_c], sort=False)
# all_data = all_data.reset_index()
# all_data.drop(inplace=True,axis=1,columns='index')

# all_data.to_csv('clean_all_data.csv', index=True)