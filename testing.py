#-*- coding: utf-8 -*-

import pandas as pd
from pandas import DataFrame
from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup
from setting import Settings

settings=Settings()

def extracting(name):
    url=setting.url_set()

    html=urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all('table')

    th_titles = table[1].find_all('th',{'class':{'title'}})
    temp_titles =[th_title.text for th_title in th_titles]

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]

    df=DataFrame(temp_numbers, index= temp_titles)

    form='''{0} 현재가{1},전일대비등락률{2},거래량{3}입니다. 거래대금{4}입니다. 전일가는 {5}었습니다. 오늘의 시가{6},고가{7},저가{8}원입니다.'''
    output=form.format(name,df.loc['현재가'][0],df.loc['등락률(%)'][0],df.loc['거래량'][0],df.loc['거래대금(백만)'][0],df.loc['전일가'][0],df.loc['시가'][0],df.loc['고가'][0],df.loc['저가'][0])


    return output

def split_stock_sentence(sentence):

    """입력된 문장을 띄어쓰기를 이용해서 분리하는 함수"""
    def finding_lopes_stock_constants(x):

        # 아랫 줄은 '어때'와 같은 settings.lopes_stock_constants 에 들어 있는
        if True in [constant == x for constant in settings.lopes_stock_constants]:
            item = 'constants'
        elif True in [function == x for function in settings.lopesStockFunctions.index]:
            item = 'function'
        else:
            item = 'item'
        return(item)

    lopes_stock_constants =[finding_lopes_stock_constants(item) for item in sentence.split(' ')]

    return (dict(zip(lopes_stock_constants, sentence.split(' '))))

def all_new(all_thing):
    if 'item' in all_thing:
        print('item이 있어요!')
        print('아이템은 '+all_thing['item'])
        if 'function' in all_thing:
            print('function도 있어요!')
            print('함수는 '+all_thing['function'])
            result = all_function(all_thing)
            if 'constants' in all_thing:
                print('constants도 있어요!')
                print(all_thing['constants'])
        elif 'constants' in all_thing:
            print('constants가 있어요!')
            print(all_thing['constants'])
    else:
        print("뭘 도와드릴까요?")
    return(result)

def all_function(all_thing):

    temp = settings.lopesStockFunctions.loc[all_thing['function'],'functions']+'('+'\''+all_thing['item']+'\''+')'
    print(temp)
    print(eval(temp))
    return(eval(temp))

def extracting_stock_code(name):
    if name in settings.KOSPI.index:
        code = settings.KOSPI.loc[name]
    else:
        code = settings.kosdaq.loc[name]
    return(code)

def price(name):
    result = extracting_stock_code(name)
    print(name)
    print(type(result))
    url= settings.url_set_naver(name)
    html=urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all('table')

    th_titles = table[1].find_all('th',{'class':{'title'}})
    temp_titles =[th_title.text for th_title in th_titles]

    td_numbers = table[1].find_all('td',{'class':{'num'}})
    temp_numbers = [td_number.text.translate({ord('\n'): ' ',ord('\t'): '' }) for td_number in td_numbers]
    #print(temp_numbers)

    df = DataFrame(temp_numbers, index= temp_titles)

    output = name+'의 '+' 현재가는 '+temp_numbers[0]+'원입니다.'
    return output
