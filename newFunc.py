from setting import Settings
import testing

settings = Settings()

def pullStockData(name):
    header = settings.deciding_catalog(name)
    code = settings.extracting_stock_code(name)
    temp = header + str(code).zfill(6)
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

def aroon(s, n=25):
    from pandas import DataFrame, Series
    from pandas.stats import moments

    up = 100 * moments.rolling_apply(s.High, n + 1, lambda x: x.argmax()) / n
    dn = 100 * moments.rolling_apply(s.Low, n + 1, lambda x: x.argmin()) / n

    return DataFrame(dict(up=up, down=dn))

def volumeOSC(name):
    df = pullStockData(name)
    temp_list = []
    for n in range(1,20):
        temp_1 = -(n+4)
        temp_2 = temp_1 - 5
        if n == 1:
            #print(temp_1,temp_2)
            value = (df['Close'][temp_1::].mean()-df['Close'][-10::].mean())/df['Close'][temp_2::].mean()
        else:
            temp_3 = temp_1 + 5
            temp_4 = temp_2 + 10
            value = (df['Close'][temp_1:temp_3].mean()-df['Close'][-10::].mean())/df['Close'][temp_2:temp_4].mean()
            #print(temp_1,temp_3,temp_2,temp_4)
        #print(value)
        temp_list.append(value)
    return(temp_list)

def investmentIndex(name):
    df = pullStockData(name)
    temp_3 = []
    for n in range(1,12):
        temp_1 = -n
        temp_2 = temp_1 - 1
        value = df['Close'][temp_1] - df['Close'][temp_2]
        #print(temp_1, temp_2)
        #print(value)
        if value > 0:
            temp_3.append(True)
    return((len(temp_3)/12*100))

def RSI(name):
    df = pullStockData(name)
    fourteenDays = df.tail(n=14)['Close']
    positive = 0
    negative = 0

    num = 13

    for n in range(0,13):
        temp = fourteenDays[num] - fourteenDays[num-1]
        if temp >= 0 :
            positive += temp
        else:
            negative += abs(temp)
        num -= 1

    #print(positive)
    #print(negative)
    #print(num)

    rsi = (positive / ( positive + negative)) * 100
    return(rsi)


def my_list():
    mines = ['현대모비스','파라다이스','신세계','LG전자']
    result_now = "< 오늘의 시황 > \\n\\n"
    result_profit = "<자네의 20거래일 수익률은 다음과 같네> \\n\\n"
    for mine in mines:
        temp_result = testing.price(mine)
        print(temp_result)
        temp_result2 = testing.percent(mine)
        temp_now = temp_result + " \\n" + temp_result2 + " \\n\\n"
        result_now += temp_now
        temp_result = profitRank_20(mine, 20)
        temp_profit = mine + ' ' + temp_result + '%' + " \\n"
        result_profit += temp_profit
        print(result_profit)

    output = result_now + '\\n\\n' + result_profit + '\\n\\n' + "자네, 주식 내공이 참 대단하네. 앞으로도 성투하게나. 무운을 비네!"
    return(output)



def interest_list():
    mines = ['SK하이닉스','아모레퍼시픽','현대위아','롯데쇼핑','KTB투자증권']
    result_profit = "< 자네가 마음쓰는 주식들의 한달간 근황일세 > \\n\\n"
    result_disparity = "< 주가의 상태도 한번 살펴보세 > \\n\\n"
    for mine in mines:
        temp_result = profitRank_20(mine, 20)
        temp_profit = mine + ' ' + temp_result + '%' + " \\n"
        result_profit += temp_profit

        temp_result = tech_disparity_20(mine, 20)
        temp_disparity = mine + ' ' + temp_result + " \\n"
        result_disparity += temp_disparity

    output = result_profit + '\\n\\n' + result_disparity + '\\n\\n' + "'주가는 이동평균선에 수렴한다' 기술적 분석 대가들의 말일세.\\n\\n20일 이동평균선을 바탕으로 '이격도(Disparity)'를 사용해 자네의 관심종목을 분석했네.\\n\\n이격도가(Disparity)는 100을 기준으로 하네. 100이 넘으면 주가의 상승세, 100 이하면 주가의 하락세를 뜻하네.\\n\\n 더불어 105가 넘어가면 과열구간. 95 이하면 과매도 구간으로 판단하네. 좀 더 완화해 110과 90을 기준으로 투자하는 경우도 있다네.\\n\\n'주식 매수의 타이밍일까, 매도의 타이밍일까?' 자네의 판단에 도움이 됐길 바라네!"

    return(output)


def cosmetics_1mth_profit(ranges = 20):
    cosmetics = ['아모레퍼시픽', 'LG생활건강', '코스맥스', '한국콜마홀딩스', '한국콜마', '콜마비앤에이치', '한국화장품', '한국화장품제조', '토니모리', '코리아나', '코스온', '제이준코스메틱', '리더스코스메틱', '네오팜', '에스디생명공학', '제닉', '에이씨티', '잇츠한불', '잉글우드랩', '글로본', '에이블씨엔씨', '클리오', '코스메카코리아', '세화피앤씨', '오가닉티코스메틱', 'SK바이오랜드', 'MP한강']
    result = "<화장품 종목의 한달 수익률 입니다> \\n"
    for cosmetic in cosmetics:
        temp_result = profitRank_20(cosmetic, ranges)
        temp_text = cosmetic +  " " + temp_result + "%" + " \\n"
        result += temp_text
    #print(result)
    return(result)
def cosmetics_1mth_profit_now(ranges = 20):
    cosmetics = ['아모레퍼시픽', 'LG생활건강', '코스맥스', '한국콜마홀딩스', '한국콜마', '콜마비앤에이치', '한국화장품', '한국화장품제조', '토니모리', '코리아나', '코스온', '제이준코스메틱', '리더스코스메틱', '에스디생명공학', '제닉', '에이씨티', '잇츠한불', '잉글우드랩', '글로본', '에이블씨엔씨', '클리오', '코스메카코리아', '세화피앤씨', '오가닉티코스메틱', 'SK바이오랜드', 'MP한강']
    result = "<화장품 종목의 지난 한달 수익률 입니다> \\n\\n"
    temp_list = {}
    rank = 1
    for cosmetic in cosmetics:
        temp_result = profitRank_20(cosmetic, ranges)
        temp_list[cosmetic] = temp_result
    results = sorted(temp_list.items(), key=operator.itemgetter(1),reverse=True)
    for k,v in results:
        temp_text = str(rank) + '위 ' + k +  " " + v + "%" + " \\n"
        result += temp_text
        rank += 1

    return(result)
def cosmetics_per_now():
    cosmetics = ['아모레퍼시픽', 'LG생활건강', '코스맥스', '한국콜마홀딩스', '한국콜마', '콜마비앤에이치', '한국화장품', '한국화장품제조', '토니모리', '코리아나', '코스온', '제이준코스메틱', '리더스코스메틱', '에스디생명공학', '제닉', '에이씨티', '잇츠한불', '잉글우드랩', '글로본', '에이블씨엔씨', '클리오', '코스메카코리아', '세화피앤씨', '오가닉티코스메틱', 'SK바이오랜드', 'MP한강']
    result = "< 화장품 종목의 PER를 들고 왔네 > \\n(11.08일 기준) \\n\\n"
    temp_list = {}
    rank = 1
    for cosmetic in cosmetics:
        temp_result = per_now(cosmetic)
        temp_list[cosmetic] = temp_result
    results = sorted(temp_list.items(), key=operator.itemgetter(1),reverse=True)
    for k,v in results:
        temp_text = str(rank) + '위 ' + k +  " PER" + v + "\\n"
        result += temp_text
        rank += 1

    result += "\\n\\n어떤가. 도움이 됐는가? \\nPER는 주가를 판단할 때 요긴하게 쓰이는 지표일세. 업종마다 PER에 대한 기준이 다르니 잘 살펴보게나!"

    return(result)

def now(name):
    #print("now함수 작동")
    if name in settings.cryptoCurrencies.index:
        #print(name)
        bithumb = cryptoCurrencies.bithumb_coins(name)
        #print(cryptoCurrencies.bithumb_coins(name))
        coinone = cryptoCurrencies.coinone_coins(name)
        #print(cryptoCurrencies.coinone_coins(name))
        output = bithumb + '\\n\\n' + coinone
        #print(output)
    else:
        output = information(name)
    return output
