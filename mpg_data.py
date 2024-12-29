import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from sklearn import metrics
from sklearn.linear_model import LinearRegression


def money_format(x):
    return "${:.2f}".format(x)


def lin_reg(X, Y):
    lr = LinearRegression()
    lr.fit(X.values.reshape(-1, 1), Y)
    intercept = lr.intercept_
    slope = lr.coef_[0]
    preds = slope * X + intercept
    rmse = round(np.sqrt(metrics.mean_squared_error(Y, preds)), 3)
    r_2 = round(metrics.r2_score(Y, preds), 2)
    return slope, intercept, preds, rmse, r_2


def get_data():
    """
    Pulls mpg data from mpg_data.csv
    and returns a formatted df
    """

    df = pd.read_csv("mpg_data.csv")

    df["miles"] = round(df["miles"].astype(float), 1)
    df["dollars"] = round(df["dollars"].astype(float), 2)
    df["gallons"] = round(df["gallons"].astype(float), 3)

    df["gal_cost"] = round(df["dollars"] / df["gallons"], 2)
    df["mpg"] = round(df["miles"] / df["gallons"], 2)

    # - 2017 Jeep Patriot tank size = 13.55 gallons
    df["tank%_used"] = round(df["gallons"] / 13.55, 4)

    df["date"] = pd.to_datetime(df["date"].astype(str))
    df["weekday"] = df["date"].dt.dayofweek.apply(
        lambda x: [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ][x]
    )
    df["days_since_last_fillup"] = df["date"].diff().dt.days
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%m/%d/%y")

    df["dollars per mile"] = round(df["dollars"] / df["miles"], 4)
    df["miles per day"] = round(df["miles"] / df["days_since_last_fillup"], 2)

    return df


def insight_creator(df):
    """
    When passed a df after going through get_data,
    this method will return a df that will provide insights on the data in different time frames
    """
    df = df.fillna(0).copy()
    df["date"] = pd.to_datetime(df["date"].astype(str))
    last_fillup = df.tail(1).copy()
    last_month = df[
        df["date"] >= pd.Timestamp(df["date"].max().date() - relativedelta(months=1))
    ].copy()
    last_3 = df[
        df["date"] >= pd.Timestamp(df["date"].max().date() - relativedelta(months=3))
    ].copy()
    last_6 = df[
        df["date"] >= pd.Timestamp(df["date"].max().date() - relativedelta(months=6))
    ].copy()
    last_year = df[
        df["date"] >= pd.Timestamp(df["date"].max().date() - relativedelta(years=1))
    ].copy()
    all_time = df.copy()

    time_periods = {
        "Most Recent Fillup": last_fillup,
        "Most Recent Month": last_month,
        "Most Recent 3 Months": last_3,
        "Most Recent 6 Months": last_6,
        "Most Recent Year": last_year,
        "All Time": all_time,
    }

    df_insights = pd.DataFrame(
        columns=[
            "Time period",
            "Miles",
            "Dollars",
            "Gallons",
            "MPG",
            "Avg gallon cost",
            "Cost to go one mile (in cents)",
            "Average miles per day",
        ]
    )

    for i in range(len(time_periods)):
        value = list(time_periods.values())[i]
        df_insights.loc[i] = [
            list(time_periods.keys())[i],
            round(sum(value["miles"]), 3),
            round(sum(value["dollars"]), 3),
            round(sum(value["gallons"]), 3),
            round(sum(value["miles"]) / sum(value["gallons"]), 3),
            round(sum(value["dollars"]) / sum(value["gallons"]), 2),
            round(sum(value["dollars"]) / sum(value["miles"]) * 100, 1),
            round(sum(value["miles"]) / sum(value["days_since_last_fillup"]), 2),
        ]

    return df_insights


def last_10_creator(df):
    last_10 = df.sort_values("date", ascending=False).head(10).copy()
    last_10["date"] = last_10["date"].dt.strftime("%b %-d, %Y").astype(str)
    last_10["miles"] = last_10["miles"].apply(lambda x: "{:,}".format(x))
    last_10["dollars"] = last_10["dollars"].apply(lambda x: "${:,.2f}".format(x))
    last_10["gallons"] = last_10["gallons"].apply(lambda x: "{:,.2f}".format(x))
    last_10["mpg"] = round(last_10["mpg"], 2)
    last_10["gal_cost"] = last_10["gal_cost"].apply(
        lambda x: "$" + str(x) + "0" if len(str(x)) < 4 else "$" + str(x)
    )
    last_10["tank%_used"] = (round(last_10["tank%_used"] * 100, 2)).astype(str) + "%"
    last_10["dollars per mile"] = "$" + (round(last_10["dollars per mile"], 2)).astype(
        str
    ).apply(lambda x: str(x) + "0" if len(str(x)) < 4 else str(x))

    return last_10[
        [
            "date",
            "miles",
            "dollars",
            "gallons",
            "mpg",
            "gal_cost",
            "tank%_used",
            "dollars per mile",
            "miles per day",
        ]
    ].copy()
