# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 19:42:04 2022

Market Making
@author: ksoo
"""

def get_balance(ticker):
    if(ticker != "KRW"):
        ticker = ticker[4::]
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:    
                return float(b['balance'])
            else:
                return 0
import numpy as np
import pandas as pd
import pyupbit
import datetime
import time
import key

access = key.access_key
secret = key.secret_key
upbit = pyupbit.Upbit(access, secret)

#tickers=pyupbit.get_tickers()
#print(tickers)\
ticker = "KRW-DOGE"
count_value = 60 * 24 * 1
df_test = pyupbit.get_ohlcv(ticker, count= count_value, interval = "minute1")
orderbook = pyupbit.get_orderbook(ticker, limit_info =True)
#ask_price = orderbook[0]['orderbook_units'][0]['ask_price']
#bid_price = orderbook[0]['orderbook_units'][0]['bid_price']

#print(ask_price)
#print(bid_price)

time_box = 10
range_box = 5
tic_value = 10
margin_value = 10
Profit_Array = list(range(0,tic_value*tic_value*margin_value))
margin = 0
tic_buy = 0
tic_sell = 2

Total_Asset = 100000
buy_count = 0
k=0
## flag init
bid_flag = 0
buy_flag = 0
sell_flag = 1
ask_flag = 1

ask_price = 0
bid_price  = 0
Total_Box = 0 
#price_init = df_test.iloc[0]['open'] - 0.5
BTC = get_balance(ticker)
krw = get_balance("KRW")
Asset_Start = BTC + krw
price_init = (orderbook[0]['orderbook_units'][0]['ask_price'] + orderbook[0]['orderbook_units'][0]['bid_price'])/2
price_current = price_init
price_buy = orderbook[0]['orderbook_units'][0]['bid_price']
price_sell = orderbook[0]['orderbook_units'][0]['ask_price']
box_flag = 0
i=0
sell_uuid = 0
buy_uuid = 0
#for i in list(range(0, count_value )):
while True:
    df_test = pyupbit.get_ohlcv(ticker, count= count_value, interval = "minute1")
    price_currnet_before = price_current
    price_buy_before = price_buy
    price_sell_before = price_sell
    price_current = (orderbook[0]['orderbook_units'][0]['ask_price'] + orderbook[0]['orderbook_units'][0]['bid_price'])/2
    price_buy = orderbook[0]['orderbook_units'][0]['bid_price']
    price_sell = orderbook[0]['orderbook_units'][0]['ask_price']
    Avg_Box = price_current
    ## Box권 설정
    #print(price_current)
    Total_Box = list(range(0,time_box))
    Sum_Box = 0
    for k in list(range(0, time_box)) :
        Total_Box[k] =  df_test.iloc[i-k]['open'] - 0.5
        Sum_Box = Sum_Box + Total_Box[k]
    Avg_Box = round(Sum_Box / time_box)
    max_list = sorted(range(len(Total_Box)), key=lambda g: Total_Box[g])[-1 * time_box:]
    min_box = Total_Box[max_list[0]]
    max_box = Total_Box[max_list[-1]]
    if(max_box < min_box + range_box):
        box_flag = 1
        #print("box")
    if(max_box >= min_box + range_box):
        box_flag = 0                 
        #print("unbox")
        #print(min_box)
        #print(max_box)
    ## Box 권에서만 동작
    #box_flag = 1
    if(box_flag == 0):
        if(upbit.get_order(ticker) != []):
            if(buy_flag == 1):            ## TBD
                upbit.cancel_order(sell_uuid['uuid'])
                time.sleep(10)
                upbit.sell_market_order(ticker,BTC*0.9)
                time.sleep(10)
                print("sell_cancle")
                #Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (price_current - bid_price)) * (1-0.001)
               #print("unbox")
            if(sell_flag == 1):            ## TBD
                upbit.cancel_order(buy_uuid['uuid'])
                print("buy_cancle")
                time.sleep(10)
                #Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (price_current - bid_price)) * (1-0.001)
                #print("unbox")
        ##flag init
        buy_flag = 0
        bid_flag = 0
        sell_flag = 1
        ask_flag = 1

    if(box_flag == 1): 
        ## 구매 Module
        if(buy_flag == 0):
            if(bid_flag ==  0):         ## 사려는 가격 책
                #bid_price = price_buy - tic_buy
                if(Avg_Box - tic_buy <= price_buy):
                    bid_price = Avg_Box - tic_buy
                    bid_flag = 1
                    krw = get_balance("KRW")
                    buy_uuid = upbit.buy_limit_order(ticker, bid_price, krw*0.9/bid_price)
                    print("buy")
                elif(Avg_Box - tic_buy > price_buy):
                    bid_price = price_buy - tic_buy
                    bid_flag = 1
                    krw = get_balance("KRW")
                    buy_uuid = upbit.buy_limit_order(ticker, bid_price, krw*0.9/bid_price)
                    print("buy")
                #print(bid_price)
            if(bid_flag == 1):        ## 살 떄 까지 대기
                if(upbit.get_order(ticker) == []):
                    buy_flag = 1
                    sell_flag = 0
                    ask_flag = 0
        ## 판매 Module
        if(sell_flag == 0):
            if(ask_flag == 0):
                if(tic_sell == 0):
                    ask_price = bid_price + 1
                elif(Avg_Box + tic_sell >= price_sell):
                    ask_price = Avg_Box + tic_sell
                    BTC = get_balance(ticker)
                    sell_uuid = upbit.sell_limit_order(ticker, ask_price, BTC*0.9)
                    print("sell")
                elif(Avg_Box + tic_sell < price_sell):
                    ask_price = price_sell + tic_sell 
                    BTC = get_balance(ticker)
                    sell_uuid = upbit.sell_limit_order(ticker, ask_price, BTC*0.9)
                    print("sell")
                ask_flag = 1    
            if(ask_flag == 1):
                if(upbit.get_order(ticker) == []):
                    bid_flag = 0
                    BTC = get_balance(ticker)
                    krw = get_balance("KRW")
                    print("nature")
                    print(price_current/price_init*100)
                    print("MMB")
                    print(BTC+krw / Asset_Start * 100)
                    #Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (ask_price - bid_price)) * (1-0.001)
                    #print(Total_Asset)
                    #print(bid_price)
                    #print(ask_price)
                    sell_flag = 1
                    buy_flag = 0
                    ask_flag = 0
                    buy_count = buy_count + 1
    #print(price_current)
    #print(Avg_Box)
    

#if(sell_flag == 0):
#    Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (price_current - bid_price)) * (1-0.001)

#Profit_Array[tic_sell * 100 + tic_buy * 10 + margin] = Total_Asset        




