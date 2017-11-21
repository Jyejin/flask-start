import pandas as pd
from pandas import DataFrame
import numpy as np
import requests
import pandas_datareader.data as web
import datetime as datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.finance import candlestick_ohlc
from setting import Settings
from flask import url_for
import json

settings = Settings()

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def pullStockData(name):
    header = settings.deciding_catalog(name)
    code = settings.extracting_stock_code(name)
    temp = header + str(code).zfill(6)
    df =settings.stocks[temp]
    return df

def df_to_np(data):
    data.reset_index(inplace=True)
    data=data.rename(columns={'index':'Date'})
    data = DataFrame(data, columns=['Date','Open','High','Low','Close','Volume'])
    data['Date']=data['Date'].dt.strftime('%Y-%m-%d')
    json_file = json.dumps([{"Date":data["Date"][i],"Open":data["Open"][i],"High":data["High"][i],"Low":data["Low"][i],"Close":data["Close"][i]} for i in range(data.shape[0])],cls=MyEncoder)

    return json_file

def h5_to_csv(data):
    data.reset_index(inplace=True)
    data=data.rename(columns={'index':'Date'})
    data = DataFrame(data, columns=['Date','Open','High','Low','Close','Volume'])
    data['Date']=data['Date'].dt.strftime('%Y-%m-%d')
    csv_file = data.to_csv(sep=',',index=False)
    return csv_file


def making_chartUrl(certainName, year='2017'):

    output = "http://lopes.hufs.ac.kr:32779/chart/"+certainName

    return output
