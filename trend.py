import pandas as pd
import json
from urllib.request import Request, urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup
from setting import Settings
import cryptoCurrencies
from flask import Blueprint

trend = Blueprint("trend",__name__)
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

@trend.route("/price/<name>")
def price(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    #description= soup.find_all('div',{'class':{'description'}})
    #date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+'의 '+' 현재가는 '+temp_numbers[0]+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[0]},ensure_ascii=False)


@trend.route("/closeyest/<name>")
def closeYest(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 전일가는 '+temp_numbers[5]+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[5]},ensure_ascii=False)

@trend.route("/priceopen/<name>")
def priceOpen(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 시초가 '+temp_numbers[7]+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[7]},ensure_ascii=False)

@trend.route("/low/<name>")
def low(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 최저가는 '+temp_numbers[11]+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[11]},ensure_ascii=False)


@trend.route("/high/<name>")
def high(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 최고가는 '+temp_numbers[9]+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[9]},ensure_ascii=False)


@trend.route("/tradingvalue/<name>")
def tradingValue(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')

    description = soup.find_all('div',{'class':{'description'}})
    date = description[0].find_all('em',{'class':{'date'}})

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 거래대금 '+temp_numbers[8].strip()+'백만원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[8].strip()},ensure_ascii=False)

@trend.route("/high52/<name>")
def high52(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 52주 최고가 '+temp_numbers[18].strip()+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[18].strip()},ensure_ascii=False)

@trend.route("/low52/<name>")
def low52(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 52주 최저가 '+temp_numbers[19].strip()+'원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[19].strip()},ensure_ascii=False)

@trend.route("/highestprice/<name>")
def highestPrice(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 상한가격은 '+temp_numbers[12]+' 원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[12]},ensure_ascii=False)

@trend.route("/lowestprice/<name>")
def lowestPrice(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 하한가격은 '+temp_numbers[14]+' 원입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[14]},ensure_ascii=False)

@trend.route("/volume/<name>")
def volume(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    output = name+' 오늘 거래량 '+temp_numbers[6]+' 입니다.'
    return json.dumps({'message':output,'numValue':temp_numbers[6]},ensure_ascii=False)

@trend.route("/percent/<name>")
def percent(name):
    soup = extracting_stock_naver(name)
    table = soup.find_all('table')
    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    if '-' in temp_numbers[4]:
        output = name+' 오늘 '+temp_numbers[4].strip()+' 내렸습니다.'
    elif '+' in temp_numbers[4]:
        output = name+' 오늘 '+temp_numbers[4].strip()+' 올랐습니다.'

    return json.dumps({'message':output,'numValue':temp_numbers[4]},ensure_ascii=False)

@trend.route("/netchange/<name>")
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

    return json.dumps({'message':output,'numValue':temp_numbers[2]},ensure_ascii=False)


@trend.route("/now/<name>")
def now(name):
    if name in settings.cryptoCurrencies.index:
        bithumb = cryptoCurrencies.bithumb_coins(name)
        coinone = cryptoCurrencies.coinone_coins(name)
        korbit = cryptoCurrencies.korbit_coins(name)
        output = bithumb + coinone +korbit
    else:
        form='''{0} 현재가 {1}원,전일대비등락률 {2}이며,전일대비 1주당 {3}원 {4}하였습니다.전일가는 {5}원이었습니다. 오늘의 거래량은 {6}입니다. 시가 {7}({8}%),고가 {9}({10}%),저가 {11}({12}%)원입니다.'''

        soup = extracting_stock_naver(name)
        table = soup.find_all('table')
        td_numbers = table[1].find_all('td',{'class':{'num'}})
        temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

        def normalize(index):
            result=temp_numbers[index]
            return int(result.replace(',', ''))

        yesterday=normalize(5)
        today=normalize(7)
        maxprice=normalize(9)
        minprice=normalize(11)

        yesper=round(((yesterday-today)/yesterday)*100,2)
        maxper=round(((yesterday-maxprice)/yesterday)*100,2)
        minper=round(((yesterday-minprice)/yesterday)*100,2)

        output = form.format(name,temp_numbers[0],temp_numbers[4].strip(),temp_numbers[2].strip()[3:],temp_numbers[2].strip()[0:2],temp_numbers[5],temp_numbers[6],temp_numbers[7],yesper,temp_numbers[9],maxper,temp_numbers[11],minper)

    return json.dumps({'message':output},ensure_ascii=False)
