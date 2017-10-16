#-*- coding: utf-8 -*-


class Settings():
    def __init__(self):
        import pandas as pd


        KOSPI=pd.read_csv("http://lopes.hufs.ac.kr/stockData/name_code_list_KOSPI.csv")
        kosdaq=pd.read_csv("http://lopes.hufs.ac.kr/stockData/name_code_list_kosdaq.csv")

        KOSPI.columns=['KOSPI','CODE']
        kosdaq.columns=['KOSDAQ','CODE']
        KOSPI.index=KOSPI['KOSPI']
        kosdaq.index=kosdaq['KOSDAQ']
        KOSPI=KOSPI['CODE']
        kosdaq=kosdaq['CODE']

        #self.name=name
        self.KOSPI = KOSPI
        self.kosdaq = kosdaq
        self.lopes_stock_constants = ['알려줘','어때','어때?']

        lopesStockFunctions = pd.read_csv("http://lopes.hufs.ac.kr/stockData/lopesStockFunction.csv", index_col= "index")
        self.lopesStockFunctions = lopesStockFunctions

    def url_set_naver(self,name):

        if name in self.KOSPI.index:
            result= self.KOSPI.loc[name]
        else:
            result=self.kosdaq.loc[name]

        url_form='http://finance.naver.com/item/sise.nhn?code=' + str(result).zfill(6)
        url=None
        url=url_form.format(result=result)

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


        url_form='https://www.samsungpop.com/mbw/trading/domesticStock.do?cmd={result}'
        url=None
        url=url_form.format(result=result)

        return url
