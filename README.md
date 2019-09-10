# mpgdata

My mission for this project is to see how my miles per gallon fluctuates over the year and throughout the seasons. Once I have enough data, I'd like to how my miles per gallon changes with the heat index for Austin, TX. I'd also like to see how the price of a gallon of gas changes over time.

[Here](https://public.tableau.com/profile/ethan.fuerst#!/vizhome/mpgdatavis/Cardashboard) is a link to the Tableau dashboard for this project

**Files in this repository:**

*moped_mpg_data.csv* - .csv that stores miles, dollars and gallons of each moped fill up as well as date 

*car_mpg_data.csv* - .csv that stores miles, dollars and gallons of each car fill up as well as date 

*mpg_extract.py* - Exports the following three .csvs each time notebook is run (will overwrite)

*clean_m_data.csv* - .csv that stores moped data to visualize

*clean_c_data.csv* - .csv that stores car data to visualize

*mpg_data.ipynb* - notebook that provides insight to mpg from clean_c_data.csv

*mpg_workbook.ipynb* - notebook where I work on adding other columns or other things

*mpg_update.command* - command file that I run on my laptop that runs mpg_extract.py to clean the data and update the .csv files and then pushes changes to github

*carmpg.twb* - tableau workbook where I visualize car mpg data and create a dashboard

*mopedmpg.twb* - tableau workbook for visualizing moped mpg data

*mpg_vis.ipynb* - notebook where I visualize data with matplotlib/seaborn and other python packages

**TODO:**

- [ ] Find accurate heat index data for Austin area to compare to my mpg data

	Status: Could use [this website](https://www.accuweather.com/en/us/austin/78701/january-weather/351193?year=2019&view=list) and use beautiful soup to scrape the data and find average temp for each day

