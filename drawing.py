import pandas as pd
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
from datetime import date
from flask import Blueprint
from pandas import DataFrame

thumbnail = Blueprint("thumbnail", __name__)
settings = Settings()

def pullStockData(name):
    header = settings.deciding_catalog(name)
    code = settings.extracting_stock_code(name)
    temp = header + str(code).zfill(6)
    df =settings.stocks[temp]
    return df

def draw_candlechart(df_ohlc, fmt='%Y%m%d', freq=7, **kwargs):
    df_ohlc = df_ohlc.reset_index()
    df_ohlc.columns = ["Date", "Adj Close", "Close" ,"High", "Low", "Open",  "Volume"]
    df_ohlc = DataFrame(df_ohlc,columns=["Date", "Open","High", "Low", "Close","Volume"])
    df_ohlc=df_ohlc[0:90]

    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    ohlc_data_arr = np.array(df_ohlc)
    ohlc_data_arr2 = np.hstack(
        [np.arange(ohlc_data_arr[:,0].size)[:,np.newaxis], ohlc_data_arr[:,1:]])
    ndays = ohlc_data_arr2[:,0]  # array([0, 1, 2, ... n-2, n-1, n])

    # Convert matplotlib date numbers to strings based on `fmt`
    dates = mdates.num2date(ohlc_data_arr[:,0])
    date_strings = []
    for date in dates:
        date_strings.append(date.strftime(fmt))
    fig, ax = plt.subplots()

    candlestick_ohlc(ax, ohlc_data_arr2, **kwargs, width=0.6, colorup='r', colordown='b')
    #candlestick_ohlc(ax, df_ohlc.values, width=0.6, colorup='r', colordown='b')
    # Format x axis
    ax.set_xticks(ndays[::freq])
    ax.set_xticklabels(date_strings[::freq], rotation=45, ha='right')
    ax.set_xlim(ndays.min(), ndays.max())

    plt.ylabel("Price")
    plt.grid(True, alpha=0.75)

    #plt.show()

    canvas=FigureCanvas(fig)

    fileName = "temp_candlestick.png"
    temp = "Temp_Folder/" + fileName
    FigureCanvas(fig).print_png(fileName, dpi=300)

    return fileName

@thumbnail.route('/<certainName>')
def making_chart(certainName, year='2017'):
    #이름이 들어가고, loc로 년도가 들어가야 한다.

    stockName = pullStockData(certainName)
    stockChart = stockName.loc[year]

    #loc 한 걸 차트 함수로 받아줘야 한다.
    return (draw_candlechart(stockChart))
