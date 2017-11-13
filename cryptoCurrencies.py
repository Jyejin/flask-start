#-*- coding:utf-8 -*-
#비트코인
# output으로 보여질 함수들이 있는 곳입니다
import pandas as pd
import json
from pandas import DataFrame
from urllib.request import Request, urlopen
from urllib.request import HTTPError
from collections import namedtuple
import datetime
from bs4 import BeautifulSoup
from setting import Settings

def bithumb(item, value):
    # https://www.bithumb.com/u1/US127
    # 1초당 20회 요청 가능합니다.
    tempURL = "https://api.bithumb.com/public/ticker/" + item
    readTicker = urlopen(tempURL).read()
    jsonTicker = json.loads(readTicker)
    output = "Bithumb에서 "+item+"의 "+value+"은 "+jsonTicker['data'][value]+"원입니다."
    return output

def bithumbMetaAPI(item):
    # https://www.bithumb.com/u1/US127
    # 1초당 20회 요청 가능합니다.
    # https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
    tempURL = "https://api.bithumb.com/public/ticker/" + item
    readTicker =urlopen(tempURL).read()
    jsonTicker = json.loads(readTicker.decode('utf-8'))
    x = json.loads(readTicker.decode('utf-8'), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return x

def bithumb_coins(name):
    cryptoCurrencies = {"비트코인":"BTC", "이더리움":"ETH",
                        "이더리움클래식":"ETC", "비트코인캐시":"BCH",
                        "리플":"XRP","퀀텀":"QTUM"}

    code = cryptoCurrencies[name]
    bithumb = bithumbMetaAPI(code)

    opening_price = float(bithumb.data.opening_price)
    closing_price = float(bithumb.data.closing_price)
    min_price = float(bithumb.data.min_price)
    max_price = float(bithumb.data.max_price)
    average_price = float(bithumb.data.average_price)
    volume_1day = float(bithumb.data.volume_1day)
    buy_price = float(bithumb.data.buy_price)
    sell_price = float(bithumb.data.sell_price)
    data = float(bithumb.data.date)

    output = "< 201_년 _월 _일 빗썸 기준> " + name +" 최근 거래가격은 "+ str(float(closing_price))+"원," + " 현재 매수 호가 최고 가격은 "+ str(float(buy_price)) + "원, " + "매도 호가 최저 가격은 " + str(float(sell_price)) + "입니다." + " 오늘의 시가는 " + str(float(opening_price)) + "원,"+ " 고가는 " + str(float(max_price)) + "원입니다." + " 저가는 " + str(float(min_price)) + "원," +  " 거래량은 " + str(float(volume_1day)) + "건 입니다."
    return output


def coinone(item, value):
    # print(str(coinoneMetaAPI("퀀텀").completeOrders))
    # 1초당 20회 요청 가능합니다.
    tempURL = "https://api.coinone.co.kr/ticker/?currency=" + item
    readTicker = urlopen(tempURL).read()
    jsonTicker = json.loads(readTicker)
    output = "coinone에서 "+item+"의 "+value+"은 "+jsonTicker['last'] + "원입니다."
    return output


def coinoneMetaAPI(name):
    # 1초당 20회 요청 가능합니다.
    # https://api.coinone.co.kr/ticker/?currency=bch&format=json
    coinone_cryptoCurrencies = {
    "비트코인캐시":"bch", "퀀텀":"qtum", "이더리움클래식":"etc",
    "비트코인":"btc", "이더리움":"eth", "리플":"xrp","시간":"timestamp"}
    code = coinone_cryptoCurrencies[name]
    tempURL = "https://api.coinone.co.kr/ticker/?currency=" + code + "&format=json"
    readTicker =urlopen(tempURL).read()
    jsonTicker = json.loads(readTicker.decode('utf-8'))
    output = json.loads(readTicker.decode('utf-8'), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return output

def coinone_coins(name):
    coinoneCryptoCurrencies = {
    "비트코인":"btc", "이더리움":"eth",
    "이더리움클래식":"etc", "비트코인캐시":"bch",
    "리플":"xrp","퀀텀":"qtum", "시간":"Timestamp"}

    code = coinoneCryptoCurrencies[name]
    coinone_coins = coinoneMetaAPI(name)

    last = float(coinone_coins.last)
    first = float(coinone_coins.first)
    low = float(coinone_coins.low)
    high = float(coinone_coins.high)
    volume = float(coinone_coins.volume)
    output = "< 201_년 _월 _일 코인원 기준> " + name +" 현 시점 거래가격은 "+ str(float(last))+"원, "+ "거래량은 " + str(float(volume)) + "입니다." " 시가는 " + str(float(first)) + "원,"+ " 저가는 " + str(float(low)) + "원," + " 고가는 " + str(float(high)) + "원입니다."
    return output

def korbitMetaAPI(name):
    # https://i.k-june.com/wp/4560
    # 현재 korbit은 api가 없습니다. 최근가만 존재합니다.
    coinone_cryptoCurrencies = {
    "비트코인캐시":"bch", "퀀텀":"qtum", "이더리움클래식":"etc",
    "비트코인":"btc", "이더리움":"eth", "리플":"xrp","시간":"timestamp"}
    # https://api.korbit.co.kr/v1/ticker?currency_pair=btc_krw
    code = coinone_cryptoCurrencies[name]
    tempURL = "https://api.korbit.co.kr/v1/ticker?currency_pair=" + code + "_krw"
    reqBTC = Request(tempURL , headers={'User-Agent': 'Mozilla/5.0'})
    readTicker =urlopen(reqBTC).read()
    jsonTicker = json.loads(readTicker.decode('utf-8'))
    output = json.loads(readTicker.decode('utf-8'), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return output


def korbit_coins(name):
    # https://i.k-june.com/wp/4560
    # 현재 korbit은 api가 없습니다. 최근가만 존재합니다.
    coinone_cryptoCurrencies = {
    "비트코인캐시":"bch", "퀀텀":"qtum", "이더리움클래식":"etc",
    "비트코인":"btc", "이더리움":"eth", "리플":"xrp","시간":"timestamp"}
    # https://api.korbit.co.kr/v1/ticker?currency_pair=btc_krw

    code = coinone_cryptoCurrencies[name]
    tempURL = "https://api.korbit.co.kr/v1/ticker?currency_pair=" + code + "_krw"
    reqBTC = Request(tempURL , headers={'User-Agent': 'Mozilla/5.0'})
    readTicker =urlopen(reqBTC).read()
    jsonTicker = json.loads(readTicker.decode('utf-8'))
    temp = datetime.datetime.fromtimestamp(int(korbitMetaAPI("이더리움").timestamp)/1000.0)

    output = "코빗(korbit)에서 "+str(temp.year)+"년 "+str(temp.month)+"월 "+str(temp.day)+"일 "+str(temp.hour)+"시 "+str(temp.second)+"분 현재, " + name + "의 거래 가격은 " + jsonTicker['last'] + "원입니다."

    return output
