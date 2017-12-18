#-*- coding:utf-8 -*-
#데이터를 불러오고 링크를 변환하는 곳입니다.
import requests

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

class Settings():
    def __init__(self):
        import pandas as pd

        KOSPI = pd.read_csv("data/name_code_list_KOSPI.csv",index_col='KOSPI_NAME')
        kosdaq = pd.read_csv("data/name_code_list_kosdaq.csv",index_col='KOSDAQ_NAME')
        cryptoCurrencies=pd.read_csv("data/cryptoCurrencies.csv", index_col='NAME')
        group_list = pd.read_csv("data/stock_sector.csv")
        explainingFunction = pd.read_csv("data/explainingFunction.csv",index_col='functionName')

        KOSPI = KOSPI['CODE']
        kosdaq = kosdaq['CODE']
        cryptoCurrencies = cryptoCurrencies['CODE']
        #h5FileUrl = 'http://lopes.hufs.ac.kr/stockData/stocks_10_27.h5'
        filename = 'data/stocks_10_27.h5'
        stocks = pd.HDFStore(filename)


        self.stocks = stocks
        self.KOSPI = KOSPI
        self.kosdaq = kosdaq
        self.cryptoCurrencies = cryptoCurrencies
        self.lopes_stock_constants = ['알려줘','어때','어때?']
        self.group_list = group_list
        self.explainingFunction = explainingFunction

        lopesStockFunctions = pd.read_csv("data/lopesStockFunction.csv", index_col= "index")
        self.lopesStockFunctions = lopesStockFunctions

    def extracting_stock_code(self,name):
        if name in self.KOSPI.index:
            code = self.KOSPI.loc[name]
        elif name in self.cryptoCurrencies.index:
            code = self.cryptoCurrencies[name]
        else:
            code = self.kosdaq.loc[name]
        return code

    def url_set_naver(self,name):

        if name in self.KOSPI.index:
            result = self.KOSPI.loc[name]
        else:
            result=self.kosdaq.loc[name]

        url_form ='http://finance.naver.com/item/sise.nhn?code=' + str(result).zfill(6)
        url = None
        url = url_form.format(result=result)

        return url

    def deciding_catalog(self,name):
        if name in self.KOSPI.index:
            catalog = "KS_"
        elif name in self.kosdaq.index:
                catalog = "KQ_"
        else:
            catalog = "None"
        return catalog

    def url_set_ss(self,data):

        result = None

        if data == 'investor':
            result= 'stockInvestorList'
        elif data == 'trader':
            result = 'stockMemberList'
        elif data == 'stockInfo':
            result = 'stockInfo'
        elif data == 'finance':
            result = 'stockFinanceList'
        elif data == 'priceList':
            result= 'stockDayList'

        url_form = 'https://www.samsungpop.com/mbw/trading/domesticStock.do?cmd={result}'
        url = None
        url = url_form.format(result=result)

        return url
