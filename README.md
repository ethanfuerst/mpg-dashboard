# mpgdata

My mission for this project is to see how my miles per gallon fluctuates over the year and throughout the seasons. Once I have enough data, I'd like to how my miles per gallon changes with the heat index for Austin, TX. I'd also like to see how the price of a gallon of gas changes over time.

[Here](https://public.tableau.com/profile/ethan.fuerst#!/vizhome/mpgdatavis/Dashboard) is a link to the Tableau dashboard for this project

**Files in this repository:**

*moped_mpg_data.csv* - .csv that stores miles, dollars and gallons of each moped fill up as well as date. I'm not doing anything with this currently, but I'm going to keep it in here for now

*car_mpg_data.csv* - .csv that stores miles, dollars and gallons of each car fill up as well as date. Once mpg_refresh.py is run, new columns are added on.

*mpg_refresh.py* - adds columns to car_mpg_data.csv and updates weather_data.csv

*mpg_insights.py* - .py file that provides insight to mpg from car_mpg_data.csv

*mpg_workbook.py* - .py file where I work on adding other columns or other things

*carmpg.twb* - tableau workbook where I visualize car mpg data and create dashboards

*mpg_vis.py* - .py file where I visualize data with matplotlib/seaborn and other python packages

*weather_data.csv* - .csv that stores the weather data

**TODO:**

- [x] delete moped data. I don't use it
- [ ] spilt tableau dashboard. One for my car and the other for mpg and weather
- [ ] change the car_mpg_data file instead of making new .csv files
- [ ] add 'cost to go one mile' on tableau dashboard and 'avg days between fillups'
