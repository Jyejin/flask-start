import pandas as pd
import json
from pandas import DataFrame
from setting import Settings
from flask import Blueprint

import operator


technicalanalysis = Blueprint("technicalanalysis", __name__)
settings = Settings()

def pullStockData(name):
    header = settings.deciding_catalog(name)
    code = settings.extracting_stock_code(name)
    temp = header + str(code).zfill(6)
    df =settings.stocks[temp]
    return df

@technicalanalysis.route("/tech-disparity/<name>/<ranges>")
def tech_disparity(name, ranges):
    '''오늘 종가와 20일동안 이격도 계산'''
    temp = pullStockData(name)
    ranges = int(ranges)
    result = round((temp['Close'][-1]/(sum(temp['Close'][-ranges::])/ranges))*100, 2)
    return json.dumps({'numValue':format(result,'0.2f')})

@technicalanalysis.route("/aroon/<s>")
def aroon(s, n=25):
    from pandas import DataFrame, Series
    from pandas.stats import moments
    s = pullStockData(s)
    up = 100 * moments.rolling_apply(s['High'], n + 1, lambda x: x.argmax()) / n
    dn = 100 * moments.rolling_apply(s['Low'], n + 1, lambda x: x.argmin()) / n

    return DataFrame(dict(up=up, down=dn))

@technicalanalysis.route("/investmentindex/<name>")
def investmentIndex(name):
    df = pullStockData(name)
    temp_3 = []
    for n in range(1,12):
        temp_1 = -n
        temp_2 = temp_1 - 1
        value = df['Close'][temp_1] - df['Close'][temp_2]
        if value > 0:
            temp_3.append(True)
    return json.dumps({'result':(len(temp_3)/12*100)})

@technicalanalysis.route("/volumeosc/<name>")
def volumeOSC(name):
    df = pullStockData(name)
    temp_list = []
    for n in range(1,20):
        temp_1 = -(n+4)
        temp_2 = temp_1 - 5
        if n == 1:
            value = (df['Close'][temp_1::].mean()-df['Close'][-10::].mean())/df['Close'][temp_2::].mean()
        else:
            temp_3 = temp_1 + 5
            temp_4 = temp_2 + 10
            value = (df['Close'][temp_1:temp_3].mean()-df['Close'][-10::].mean())/df['Close'][temp_2:temp_4].mean()
        temp_list.append(value)
    return json.dumps({'result':temp_list})
