# %%
from IPython import get_ipython
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
get_ipython().run_line_magic('matplotlib', 'inline')


# %%
df_m = pd.read_csv('clean_m_data.csv',index_col = 0)
df_m.name = 'Moped Data'
df_c = pd.read_csv('clean_c_data.csv',index_col = 0)
df_c.name = 'Car Data'


# %%
df_m.head()


# %%
df_c.head()


# %%
for i in [df_m, df_c]:
    print(i.name + ':')
    print("Total miles: " + str(round(sum(i.miles), 2)) + " miles")
    print("Total spent on gas: $" + str(round(sum(i.dollars), 2 )))
    print("Total gallons pumped: " + str(round(sum(i.gallons), 2)) + " gallons")
    print("Miles per gallon: " + str(round(sum(i.miles)/sum(i.gallons), 2)))
    print("Average cost of one gallon of gas: $" + str(round(sum(i.dollars)/sum(i.gallons), 2)))
    print("Cost to go one mile: $" + str(round(sum(i.dollars)/sum(i.miles), 2)))
    print()


# %%



