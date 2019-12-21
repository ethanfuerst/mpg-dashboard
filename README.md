# mpgdata

My mission for this project is to see how my miles per gallon fluctuates over the year and throughout the seasons. Once I have enough data, I'd like to how my miles per gallon changes with the heat index for Austin, TX. I'd also like to see how the price of a gallon of gas changes over time.

[Here](https://public.tableau.com/profile/ethan.fuerst#!/vizhome/mpgdatavis/Dashboard) is a link to the Tableau dashboard for this project

**Files in this repository:**

_*car_mpg_data.csv*_ - .csv that stores miles, dollars and gallons of each car fill up as well as date. Once mpg_refresh.py is run, new columns are added on.

_*moped_mpg_data.csv*_ - .csv that stores miles, dollars and gallons of each moped fill up as well as date. I'm not doing anything with this currently, but I'm going to keep it in here for now

_*mpg_refresh.py*_ - adds columns to car_mpg_data.csv and updates weather_data.csv

_*mpg_insights.py*_ - .py file with method that provides insight to mpg when passed a df

_*carmpg.twb*_ - tableau workbook where I visualize car mpg data and create dashboards

_*mpg_vis.py*_ - .py file where I visualize data with matplotlib/seaborn and other python packages

_*weather_data.csv*_ - .csv that stores the weather data

_*car_data.py*_ - .py file that prints out car data mpg_insights

_*moped_data.py*_ - .py file that prints out moped data mpg_insights

_*mpg_workbook.py*_ - .py file where I work on adding other columns or other things

**TODO:**

- [x] delete moped data. I don't use it
- [ ] spilt tableau dashboard. One for my car and the other for mpg and weather
- [ ] change the car_mpg_data file instead of making new .csv files
- [ ] add 'cost to go one mile' on tableau dashboard and 'avg days between fillups'
