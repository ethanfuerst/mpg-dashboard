import pandas as pd

from mpg_data import get_data

BUY_PRICE = 12200
FINAL_SALE_PRICE = 11000
df = get_data()

dep_per_mile = (BUY_PRICE - FINAL_SALE_PRICE) / df["miles"].sum()

df["depreciation"] = df["miles"] * dep_per_mile
df["tot_dep"] = df["depreciation"].cumsum()
df["sale_price"] = BUY_PRICE - df["tot_dep"]

date_spine = pd.DataFrame(
    {"date": pd.date_range(start=df["date"].min(), end=df["date"].max(), freq="D")}
)
date_spine["date"] = pd.to_datetime(date_spine["date"]).dt.date

# avg of 15% depreciation per year
# add in daily depreciation

# look at longest times without fillups

# look at clusters of freqent fillups

# dist of tank % used, mpg, gal cost, miles
