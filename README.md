# mpgdata

My mission for this project is to see how my miles per gallon fluctuates over the year and throughout the seasons. Once I have enough data, I'd like to how my miles per gallon changes with the heat index for Austin, TX. I'd also like to see how the price of a gallon of gas changes over time.

[Here](https://public.tableau.com/profile/ethan.fuerst#!/vizhome/mpgdatavis/Cardashboard) is a link to the Tableau dashboard for this project

**Files in this repository:**

*moped_mpg_data.csv* - .csv that stores miles, dollars and gallons of each moped fill up as well as date 

*car_mpg_data.csv* - .csv that stores miles, dollars and gallons of each car fill up as well as date 

*mpg_data.ipynb* - notebook that creates new columns in pandas dataframes for analysis. Exports the following three .csvs each time notebook is run (will overwrite)

*clean_m_data.csv* - .csv that stores moped data to visualize

*clean_c_data.csv* - .csv that stores car data to visualize

*clean_all_data.csv* - .csv that stores data in clean_m_data.csv and clean_c_data.csv, has extra column to differentiate which vehicle fill up was for

*mpgdatavis.twb* - tableau workbook where I visualize all data and create a dashboard

*mpg_vis.ipynb* - notebook where I visualize data with matplotlib/seaborn and other python packages

**TODO:**

- [ ] update the dashboard online with new data i've collected
	
	status: posted question on tableau online forum

- [ ] find accurate heat index data for Austin area to compare to my mpg

	status: still looking for heat index data. might have to use temp each day instead, averaged over period between fillups