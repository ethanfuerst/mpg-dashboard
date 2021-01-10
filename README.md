# mpg-dashboard

My mission for this project is to build a dashboard using Plotly and Dash that will showcase the miles per gallon data from my car. Each time I fill up my car I record the miles I have driven since I last filled up, the gallons of gas I'm putting in my car, the price of the gas, and the date. With just this data, I'm able to create a lot of cool insights!

[Here](https://tidbitstatistics-mpg-dash.herokuapp.com/) is a link to the dashboard for this project

## Files in this repository by extension

### .py

__*app.py*__ - my [mpg dashboard](https://tidbitstatistics-mpg-dash.herokuapp.com/)

__*mpg_data.py*__ - pulls and formats data from google sheet

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
- [x] remake tableau dashboard in plotly in mpg_vis.ipynb
  - [x] sync two line graphs in tableau dashboard in plotly
  - [x] figure out how to host vizs on blog using plotly graphs
- [x] make mpg_insight plotly table
- [x] make dash dashboard
- [x] move app to this directory
- [ ] compare linear regression of metrics over different times
- [ ] make 3D plot with miles driven, cost to go one mile and mpg
  - [ ] clustering?
- [ ] bring weather back in?
  - [ ] find new API for weather
