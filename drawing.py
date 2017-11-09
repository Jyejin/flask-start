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

settings = Settings()

def pullStockData(name):
    header = settings.deciding_catalog(name)
    code = settings.extracting_stock_code(name)
    temp = header + str(code).zfill(6)
    df =settings.stocks[temp]
    return df

def chart(stock_df):
    #Reset the index to remove Date column from index
    df_ohlc = stock_df.reset_index()

    # Naming columns
    # df_ohlc.columns = ["Date","Open","High",'Low',"Close"]
    df_ohlc.columns = ["Date", "Adj Close", "Close" ,"High", "Low", "Open",  "Volume"]

    #Converting dates column to float values
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    #Making plot
    fig = plt.figure()
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
    #ax1.grid(True)

    #Converts raw mdate numbers to dates
    ax1.xaxis_date()
    plt.xlabel("Date")

    #Making candlestick plot
    candlestick_ohlc(ax1,df_ohlc.values,width=1, colorup='#2B64DF', colordown='#D5161B')
    # 다음 값은 네이버 값입니다.
    #2B64DF #D5161B
    plt.ylabel("Price")
    ##아래 것이 무엇인지 잘 모르겠다.
    plt.legend(['negative','positive'])
    plt.grid(True, alpha=0.75)
    # 파일이 안 나올 때 아래 명령을 이용해서 확인한다.
    #plt.show()

    canvas=FigureCanvas(fig)

    fileName = "temp_candlestick.png"
    #temp = "Temp_Folder/" + fileName
    FigureCanvas(fig).print_png(fileName, dpi=300)

    return fileName

def making_chart(certainName, year='2017'):
    #이름이 들어가고, loc로 년도가 들어가야 한다.

    stockName = pullStockData(certainName)
    stockChart = stockName.loc[year]

    #loc 한 걸 차트 함수로 받아줘야 한다.
    return (chart(stockChart))

#print(making_chart("삼성전자"))
