import requests
import pandas as pd
import simplejson as json
#from bokeh.plotting import figure
#from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session
from bokeh.plotting import figure, output_file, show 

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
      return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    print ("This is index function")  
    return render_template('index.html')
   
@app.route('/graph', methods=['POST'])
def graph():
    print ("This is the graph function")
    print (request.form.get('features'))
#    if request.method == 'POST':
    app.vars['ticker'] = request.form['ticker']
    API_KEY = 'ZQ0KZVXCAMRYI5DQ'
    #ticker = 'IBM'
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_Daily&symbol=' + app.vars['ticker']+ '&apikey=' + API_KEY)
    #print(r.status_code)
    result = r.json()
    dataForAllDays = result['Time Series (Daily)']

    df = pd.DataFrame.from_dict(dataForAllDays, orient='index') 
    #df = df.sort_values(by=['date'])

    df = df.reset_index()
    #rename columns
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})
    # #Changing to datetime
    df['date'] = pd.to_datetime(df['date'])
    # #Sort according to date
    # #df = df.sort_values(by=['date'])
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(int)  

    # get the last 30 day 
    df1= df.iloc[0:29] # last 30 days 

    p = figure(title='Stock prices for %s' % app.vars['ticker'],
        x_axis_label='date',
        x_axis_type='datetime')

    #p.line(x=df['date'].values, y=df['close'].values,line_width=4, legend='Close')    
    #if request.method == 'POST': 
 
    if request.form.get('features') == 'Close':
        p.line(x=df1['date'].values, y=df1['close'].values,line_width=2, legend='Close')
        # print ("Select Close for this plot")
    if request.form.get('features') == 'Open':
       p.line(x=df1['date'].values, y=df1['open'].values,line_width=2, line_color="green", legend='Open')
    if request.form.get('features') =='High':
        p.line(x=df1['date'].values, y=df1['high'].values,line_width=2, line_color="red", legend='High')
    if request.form.get('features') =='Low':
        p.line(x=df1['date'].values, y=df1['low'].values,line_width=2, line_color="purple", legend='Low')
        
    script, div = components(p)    

    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)