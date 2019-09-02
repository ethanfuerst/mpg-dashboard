# mpgdata

My mission for this project is to see how my miles per gallon fluctuates over the year and throughout the seasons. Once I have enough data, I'd like to how my miles per gallon changes with the heat index for Austin, TX. I'd also like to see how the price of a gallon of gas changes over time.

[Here](https://public.tableau.com/profile/ethan.fuerst#!/vizhome/mpgdatavis/Cardashboard) is a link to the Tableau dashboard for this project

**Files in this repository:**

*moped_mpg_data.csv* - .csv that stores miles, dollars and gallons of each moped fill up as well as date 

*car_mpg_data.csv* - .csv that stores miles, dollars and gallons of each car fill up as well as date 

*mpg_extract.py* - Exports the following three .csvs each time notebook is run (will overwrite)

*clean_m_data.csv* - .csv that stores moped data to visualize

*clean_c_data.csv* - .csv that stores car data to visualize

*clean_all_data.csv* - .csv that stores data in clean_m_data.csv and clean_c_data.csv, has extra column to differentiate which vehicle fill up was for

*mpg_data.ipynb* - notebook that provides insight to mpg from clean_c_data.csv and clean_m _data.csv 

*mpg_workbook.ipynb* - notebook where I work on adding other columns or other things

*mpg_extract.command* - command file that I run on my laptop that runs mpg_extract.py to clean the dat and update the .csv files and then pushes changes to github

*mpgdatavis.twb* - tableau workbook where I visualize all data and create a dashboard

*mpg_vis.ipynb* - notebook where I visualize data with matplotlib/seaborn and other python packages

**TODO:**

- [ ] Find accurate heat index data for Austin area to compare to my mpg data

	Status: Still looking for heat index data. Might have to use temp each day instead, averaged over period between fillups

