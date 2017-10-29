#-*- coding:utf-8 -*-
#데이터를 불러오고 링크를 변환하는 곳입니다.
class Settings():
    def __init__(self):
        import pandas as pd


        KOSPI = pd.read_csv("http://lopes.hufs.ac.kr/stockData/name_code_list_KOSPI.csv",index_col='KOSPI_NAME')
        kosdaq = pd.read_csv("http://lopes.hufs.ac.kr/stockData/name_code_list_kosdaq.csv",index_col='KOSDAQ_NAME')

        KOSPI = KOSPI['CODE']
        kosdaq = kosdaq['CODE']

        #self.name=name
        self.KOSPI = KOSPI
        self.kosdaq = kosdaq
        self.lopes_stock_constants = ['알려줘','어때','어때?']

        lopesStockFunctions = pd.read_csv("http://lopes.hufs.ac.kr/stockData/lopesStockFunction.csv", index_col= "index")
        self.lopesStockFunctions = lopesStockFunctions

    def extracting_stock_code(self,name):
        if name in self.KOSPI.index:
            code = self.KOSPI.loc[name]
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

    def url_set_ss(self,data):

        result=None

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
