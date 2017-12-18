from setting import Settings
import operator
from flask import Blueprint
import json

profit = Blueprint("profit", __name__)
settings = Settings()

def pullStockData(name):
    header = settings.deciding_catalog(name)
    code = settings.extracting_stock_code(name)
    temp = header + str(code).zfill(6)
    df =settings.stocks[temp]
    return df

@profit.route("/profitdays/<name>/<ranges>")
def profitRank(name, ranges):
    '''오늘 종가와 20일전 영업날 계산'''
    temp = pullStockData(name)
    ranges=int(ranges)+1
    result = round((temp['Close'][-1] - temp['Close'][-ranges])/temp['Close'][-1]*100, 2)

    return json.dumps({'numValue':format(result,'0.2f')})
