
#-*- coding:utf-8 -*-
# output으로 보여질 함수들이 있는 곳입니다
import pandas as pd
import json
from pandas import DataFrame
from urllib.request import Request, urlopen
from urllib.request import HTTPError
from collections import namedtuple
from bs4 import BeautifulSoup
from setting import Settings
import drawing


settings = Settings()


def extracting_stock_naver(name):

    url = settings.url_set_naver(name)
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    return soup


def split_stock_sentence(sentence):

    """입력된 문장을 띄어쓰기를 이용해서 분리하는 함수"""
    def finding_lopes_stock_constants(x):

        # 아랫 줄은 '어때'와 같은 settings.lopes_stock_constants 에 들어 있는
        if True in [constant == x for constant in settings.lopes_stock_constants]:
            item = 'constants'
        elif True in [function == x for function in settings.lopesStockFunctions.index]:
            item = 'function'
        elif bool(x in settings.KOSPI.index or x in settings.kosdaq.index or x in settings.cryptoCurrencies.index):
            item = 'item'
        else:
            item = 'error'
        return item

    lopes_stock_constants =[finding_lopes_stock_constants(item) for item in sentence.split(' ')]

    return (dict(zip(lopes_stock_constants, sentence.split(' '))))


def all_function(all_thing):
    sentence = split_stock_sentence(all_thing)

    if 'item' in sentence.keys() and not 'function' in sentence.keys():
        temp = information(sentence['item'])

    elif 'item' in sentence.keys() and 'function' in sentence.keys() :
        temp = eval(settings.lopesStockFunctions.loc[sentence['function'],'functions']+'('+'\''+sentence['item']+'\''+')')
    else:
        temp = "다시 입력해 주세요"
    return temp

def extracting_stock_code(name):
    if name in settings.KOSPI.index:
        code = settings.KOSPI.loc[name]
    elif name in settings.cryptoCurrencies.index:
        code = settings.cryptoCurrencies.loc[name]
    else:
        code = settings.kosdaq.loc[name]
    return code

# 이 아래에는 각자 돌아가는 함수만 넣습니다.

def information(name):
    if name in settings.cryptoCurrencies.index:
        code = extracting_stock_code(name)
        output = name + code + "의 information() 입니다."
    else:
        soup = extracting_stock_naver(name)
        table = soup.find_all('table')

        description= soup.find_all('div',{'class':{'description'}})
        date = description[0].find_all('em',{'class':{'date'}})
        td_numbers = table[1].find_all('td',{'class':{'num'}})
        temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

        output = "<2017.09월 3분기 기준> "+name + ' 시가총액 '+ temp_numbers[20] +', 자본금 '+temp_numbers[23]+', 상장주식수 '+temp_numbers[22]+ \
                ', 액면가'+temp_numbers[10]+', PER(주가수익비율) '+ temp_numbers[16] + ', EPS(주당순이익)' + temp_numbers[17]+\
                '원입니다. 52주 최고가 ' +  temp_numbers[18] +', 52주 최저가 '+temp_numbers[19]+'입니다. ' +  date[0].text + name +' 현재가 '+ temp_numbers[0]+'원입니다.'

    return output

def marketCap(name):
    result = extracting_stock_code(name)
    url_form = settings.stock_sise_naver_url + str(result).zfill(6)
    url = None
    url = url_form.format(result=result)
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # 장마감 문장 뽑아오기!
    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})
    # print(date[0].text) #뽑아온 것 확인하는 코드

    table = soup.find_all('table')

    th_titles = table[1].find_all('th',{'class':{'title'}})
    temp_titles = [th_title.text for th_title in th_titles]

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]
    #print(temp_numbers)
    # 아래 df는 자료가 잘 들어왔는지 확인하는 DataFrame
    #df = DataFrame(temp_numbers, index= temp_titles)
    # 삼성전자 시가총액은 3,503,749억원입니다. <2017년 10월 17일 기준>
    output = name+' 시가총액은 '+temp_numbers[20]+' 입니다.'+'[' + date[0].text + ']'

    return output

def price(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    #description= soup.find_all('div',{'class':{'description'}})
    #date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+'의 '+' 현재가는 '+temp_numbers[0]+'원입니다.'
    return output

def per(name):

    soup = extracting_stock_naver(name)
    # 장마감 문장 뽑아오기!
    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})
    # print(date[0].text) #뽑아온 것 확인하는 코드

    table = soup.find_all('table')

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]
    #print(temp_numbers)

    #삼성전자의 PER(주가수익비율)는 19.74입니다.
    output = name+'의 '+'PER(주가수익비율)는 '+temp_numbers[16]+'입니다.'+'[' + date[0].text + ']'
    return output

def closeYest(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 전일가는 '+temp_numbers[5]+'원입니다.'
    return output

def priceOpen(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 시초가 '+temp_numbers[7]+'원입니다.'
    return output

def low(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 최저가는 '+temp_numbers[11]+'원입니다.'
    return output

def high(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 최고가는 '+temp_numbers[9]+'원입니다.'
    return output

def tradingValue(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 거래대금 '+temp_numbers[8].strip()+'백만원입니다.'
    return output

def high52(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 52주 최고가 '+temp_numbers[18].strip()+'원입니다.'
    return output

def low52(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 52주 최저가 '+temp_numbers[19].strip()+'원입니다.'
    return output

def shares(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 주식 수 '+temp_numbers[21].strip()+'주입니다.'
    return output

def marketCap(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 시가총액 '+temp_numbers[20].strip()+'원입니다.'
    return output

def eps(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' EPS(주당순이익)는 '+temp_numbers[17].strip()+'입니다.'
    return output

def foreignShare(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 외국인 주식수 '+temp_numbers[22].strip()+'입니다.'
    return output

def parValue(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 액면가 '+temp_numbers[10].strip()+'입니다.'
    return output

def capitalStock(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 자본금 '+temp_numbers[23].strip()+'원입니다.'
    return output

def highestPrice(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 상한가격은 '+temp_numbers[12]+' 원입니다.'
    return output

def lowestPrice(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 하한가격은 '+temp_numbers[14]+' 원입니다.'
    return output

def volume(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 거래량 '+temp_numbers[6]+' 입니다.'
    return output

def percent(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    if '-' in temp_numbers[4]:
        output = name+' 오늘 '+temp_numbers[4].strip()+' 내렸습니다.'
    elif '+' in temp_numbers[4]:
        output = name+' 오늘 '+temp_numbers[4].strip()+' 올랐습니다.'

    return output

def netchange(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    if '하락' in temp_numbers[2]:
        output = name+' 오늘 1주당 '+temp_numbers[2].strip()+'원 내렸습니다.'
        output = output.replace('하락','')

    elif '상승' in temp_numbers[2]:
        output = name+' 오늘 1주당 '+temp_numbers[2].strip()+'원 올랐습니다.'
        output = output.replace('상승 ','')

    return output

def now(name):
    if name in settings.cryptoCurrencies.index:
        bithumb = bithumb_coins(name)
        coinone = coinone_coins(name)
        korbit = korbit_coins(name)
        output = bithumb + coinone +korbit
    else:
        code = extracting_code(name)
        output = price(name)
    return output 
