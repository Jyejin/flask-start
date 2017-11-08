from setting import Settings

settings = Settings()

def pullStockData(name):
    header = settings.deciding_catalog(name)
    code = settings.extracting_stock_code(name)
    temp = header + str(code).zfill(6)
    print(temp)
    df =settings.stocks[temp]
    return df

def profitRank_5(name, ranges = 5):
    '''오늘 종가와 20일전 영업날 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1] - temp['Close'][-ranges::])/temp['Close'][-1]*100, 2)
    return(format(result,'0.2f'))

def profitRank_10(name, ranges = 10):
    '''오늘 종가와 20일전 영업날 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1] - temp['Close'][-ranges::])/temp['Close'][-1]*100, 2)
    return(format(result,'0.2f'))

def profitRank_20(name):
    '''오늘 종가와 20일전 영업날 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1] - temp['Close'][-21])/temp['Close'][-1]*100, 2)
    return(format(result,'0.2f'))

def profitRank_60(name):
    '''오늘 종가와 20일전 영업날 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1] - temp['Close'][-61])/temp['Close'][-1]*100, 2)
    return(format(result,'0.2f'))

def profitRank_120(name):
    '''오늘 종가와 20일전 영업날 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1] - temp['Close'][-121])/temp['Close'][-1]*100, 2)
    return(format(result,'0.2f'))

def profitRank_250(name):
    '''오늘 종가와 20일전 영업날 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1] - temp['Close'][-251])/temp['Close'][-1]*100, 2)
    return(format(result,'0.2f'))

def tech_disparity(name, ranges = 20):
    '''오늘 종가와 20일동안 이격도 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1]/(sum(temp['Close'][-ranges::])/ranges))*100, 2)
    return(format(result,'0.2f'))

def tech_disparity_5(name, ranges = 5):
    '''오늘 종가와 20일동안 이격도 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1]/(sum(temp['Close'][-ranges::])/ranges))*100, 2)
    return(format(result,'0.2f'))

def tech_disparity_10(name, ranges = 10):
    temp = pullStockData(name)
    result = round((temp['Close'][-1]/(sum(temp['Close'][-ranges::])/ranges))*100, 2)
    return(format(result,'0.2f'))

def tech_disparity_15(name, ranges = 15):
    '''오늘 종가와 20일동안 이격도 계산'''
    temp = pullStockData(name)
    result = round((temp['Close'][-1]/(sum(temp['Close'][-ranges::])/ranges))*100, 2)
    return(format(result,'0.2f'))
