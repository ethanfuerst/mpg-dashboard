# mpg_data

My mission for this project is to see how my miles per gallon fluctuates over the year and throughout the seasons. Once I have enough data, I'd like to how my miles per gallon changes with the weather in Austin, TX. I'd also like to see how the price of a gallon of gas changes over time.

[Here](https://public.tableau.com/profile/ethan.fuerst#!/vizhome/mpgdatavis/GasTankDashboard) is a link to the Tableau dashboard for this project

## Files in this repository

### .csvs

__*car_mpg_data.csv*__ - .csv that stores miles, dollars and gallons of each car fill up as well as date. Once mpg_refresh.py is run, new columns are added on.

__*mpg_insights.csv*__ - .csv that stores insights about my mpg data

### Jupyter notebooks

__*mpg_vis.ipynb*__ - mpg data visualized with plotly/matplotlib

__*mpg_workbook.ipynb*__ - mpg data workstation

### Python files

__*mpg_refresh.py*__ - adds columns to car_mpg_data.csv. run after new mpg data is recorded.

### Tableau files

__*carmpg.twb*__ - dashboards and various vizs for data

__*Gas Tank Dashboard.twb*__ - tableau workbook with finalized Dashboard that is published to [my Tableau Public profile](https://public.tableau.com/profile/ethan.fuerst/)

## TODO

- [x] delete moped data. I don't use it
- [x] spilt tableau dashboard. One for my car and the other for mpg and weather
- [X] change the car_mpg_data file instead of making new .csv files
- [x] fix get_weather
  - [x] add to own repository
- [x] add 'cost to go one mile' on tableau dashboard
  - [x] create df with one row, column names are insights and the values are the numbers. Add as table to dashboard
  - [x] create extra rows like 'in last month', one for 'in last year', etc.
- [x] remove weather data
- [x] clean up mpg_refresh.py
  - [x] clean up mpg_data_creator()
- [x] change .py files to .ipynb
- [ ] remake tableau dashboard in plotly in mpg_vis.ipynb
  - [x] sync two line graphs in tableau dashboard in plotly
  - [x] figure out how to host vizs on blog using plotly graphs
  - [ ] figure out why .ipynb files are not showing plotly figures
  - [ ] display last x days automatically, can zoom out for more
- [ ] make mpg_insight plotly table
- [ ] bring weather back in
  - [ ] find new API for weather
