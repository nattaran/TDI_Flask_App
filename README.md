# TDI Milestone Project - Fall 2020 
## Flask on Heroku

The project allows the user to display the 30-day price history for a stock. The user can input any value into the 'ticker' field, and select any particular price option. The program then displays the data.

app.py
This accepts the user ticker value, formats into an API string, and sends a request to Alpha vintage. The request is returned in .json format, which is then read into pandas. The company name is extracted as well. The relevant columns are extracted from pandas, and a plot is calculated using bokeh. The plot data and compnay name are fed to plot.html.


Produced as part of the Data Incubator course.

The app can be seen here (https://nasrin-tdi-app.herokuapp.com/) 

