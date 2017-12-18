import pandas as pd
import json
from pandas import DataFrame
from urllib.request import Request, urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup
from setting import Settings
import cryptoCurrencies

from flask import Blueprint

fundamentalanalysis = Blueprint("fundamentalanalysis",__name__)
settings = Settings()

def extracting_stock_naver(name):

    url = settings.url_set_naver(name)
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    return soup

def extracting_stock_code(name):
    if name in settings.KOSPI.index:
        code = settings.KOSPI.loc[name]
    elif name in settings.cryptoCurrencies.index:
        code = settings.cryptoCurrencies.loc[name]
    else:
        code = settings.kosdaq.loc[name]
    return code

@fundamentalanalysis.route("/shares/<name>")
def shares(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 주식 수 '+temp_numbers[21].strip()+'주입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[21].strip()},ensure_ascii=False)

@fundamentalanalysis.route("/marketcap/<name>")
def marketCap(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 시가총액 '+temp_numbers[20].strip()+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[20].strip()},ensure_ascii=False)

@fundamentalanalysis.route("/capitalstock/<name>")
def capitalStock(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 자본금 '+temp_numbers[23].strip()+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[23].strip()},ensure_ascii=False)

@fundamentalanalysis.route("/foreignshare/<name>")
def foreignShare(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 외국인 주식수 '+temp_numbers[22].strip()+'입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[22].strip()},ensure_ascii=False)

@fundamentalanalysis.route("/pervalue/<name>")
def parValue(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 액면가 '+temp_numbers[10].strip()+'입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[10].strip()},ensure_ascii=False)

@fundamentalanalysis.route("/per/<name>")
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
    return json.dumps({'message':output,'numValue':temp_numbers[16].strip()},ensure_ascii=False)

@fundamentalanalysis.route("/eps/<name>")
def eps(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' EPS(주당순이익)는 '+temp_numbers[17].strip()+'입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[17].strip()},ensure_ascii=False)

@fundamentalanalysis.route("/information/<name>")
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

    return json.dumps({'message':output},ensure_ascii=False)

@fundamentalanalysis.route("/explaining/<name>")
def explaining(name):
    """
    함수 이름만 불렀을 경우에 그 함수에 대한 설명을 해주는 함수입니다.
    """
    if name in settings.explainingFunction.index:
            result = settings.explainingFunction.loc[name]['functionExplain']


    else:
        temp = name + ' 함수는 아직 설명이 없습니다!'
        result = {name: temp}
    return json.dumps({'statement':result},ensure_ascii=False)
