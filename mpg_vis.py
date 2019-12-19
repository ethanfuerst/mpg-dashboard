# %%
from IPython import get_ipython
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
get_ipython().run_line_magic('matplotlib', 'inline')

df_m = pd.read_csv('clean_m_data.csv')
df_m.name = 'Moped Data'
df_c = pd.read_csv('clean_c_data.csv')
df_c.name = 'Car Data'


# %%
# Looking to see how cost of a gallon changes over time

plt.figure(figsize=(20,10))
plt.plot(df_c['date'], df_c['gal_cost'], 'r')
plt.xlabel('Date')
plt.ylabel('Gallons')
plt.title('Gallon cost vs. Time')
plt.show()


# %%
# Moving average of mpg
# Need to group by months

plt.figure(figsize=(20,10))
plt.plot(df_c['date'], df_c['mpg'].rolling(window=3).mean(), 'b')
plt.xlabel('Date')
plt.ylabel('Miles per gallon')
plt.title('Moving average of mpg vs. time')
plt.show()


# %%
# Moving average of mpg
# Need to group by months

plt.figure(figsize=(20,10))
plt.plot(df_c['date'], df_c['gal_cost'].rolling(window=3).mean(), 'g')
plt.xlabel('Date')
plt.ylabel('Miles per gallon')
plt.title('Moving average of mpg vs. time')
plt.show()


# %%
# moving average chart for car mpg and cost for gallon of gas
# also chart with moving average for mpg but a mark on chart gal cost


