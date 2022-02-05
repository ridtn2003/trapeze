# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 23:07:29 2022

@author: ksoo
"""


def get_balance(ticker):
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

ticker = "KRW-BTC"

#k_ratio = k_ratio+1
#cnt = 0
#Asset_Start = 100000
#Asset_End = 100000
#KRW = 100000
#BTC = 0
#KRW_before = 100000
#BTC_before = 0
Buy_Flag = 0
Sell_Flag = 1
Buy_count = 0
Sell_count = 0
count_buy = 0
k_ratio_Before = 0
ticker_origin = "BTC"
cnt = 0
VG_Price_Start = pyupbit.get_current_price("KRW-BTC")
#print(get_balance('BTC'))
ksoo_balance_Start = get_balance('KRW') + get_balance('BTC') * pyupbit.get_current_price('KRW-BTC') 
BTC = get_balance(ticker_origin)


while True:
    try:
        now = datetime.datetime.now()
        if(cnt% 3600 == 0 ):
            print(now)
        cnt = cnt+1
        f=open("k.log",'r')
        line = f.readline()
        line = line.strip('\n')
        k_ratio = float(line)
        if(k_ratio != k_ratio_Before):
            print(k_ratio)
            k_ratio_Before = k_ratio
        f.close()
    #while cnt < 1000000:
        #line = f.readline()
        #if not line: break
        #cnt = cnt+1
        #line = line.strip('\n')
    #    print(line)
        krw = get_balance("KRW")
        orderbook = pyupbit.get_orderbook("KRW-BTC", limit_info =True)
        #df = pyupbit.get_ohlcv("KRW-BTC", count=1, interval = "minute1")
        Price = pyupbit.get_current_price("KRW-BTC")
        ask_amount = orderbook[0]['total_ask_size']
        bid_amount = orderbook[0]['total_bid_size']
        count_buy = 0
        if(bid_amount > k_ratio * ask_amount and Sell_Flag == 1):  ## BTC 사라
            Sell_Flag = 0
            Buy_Flag = 1
            print("buy")
            krw_buy = krw
            count_buy=1
            upbit.buy_market_order(ticker,krw*0.9)
            #flag = "BTC"
            #Buy_count = Buy_count + 1
            #print("Buy")
        if(bid_amount * k_ratio < ask_amount and Buy_Flag == 1):  ## BTC 팔아라
            Sell_Flag = 1
            Buy_Flag = 0
            print("sell")
            count_buy=2
            upbit.sell_market_order(ticker,BTC*0.9)
            #flag = "KRW"
            #Sell_count = Sell_count + 1
            #print("Sell")
        krw = get_balance("KRW")
        krw_sell = krw
        #Asset_End = KRW + BTC * Price   ## 자산 총액
        #print(Asset_End)
        #print(KRW)
        #print(BTC)
        #print(Price)
        if(count_buy == 2):
            if(krw_buy < krw_sell):
                print("good")
                ksoo_balance = get_balance('KRW') + get_balance('BTC') * pyupbit.get_current_price('KRW-BTC') 
                ksoo_balance = 'ksoo balance = ' + str(ksoo_balance)
                print("Profit of AB")
                print(ksoo_balance/ksoo_balance_Start*100)
                print("Profit of Nature")
                print(Price/VG_Price_Start*100)
                print(ksoo_balance)
            if(krw_buy > krw_sell):
                print("bad")
                ksoo_balance = get_balance('KRW') + get_balance('BTC') * pyupbit.get_current_price('KRW-BTC') 
                ksoo_balance = 'ksoo balance = ' + str(ksoo_balance)
                print("Profit of AB")
                print(ksoo_balance/ksoo_balance_Start*100)
                print("Profit of Nature")
                print(Price/VG_Price_Start*100)
                print(ksoo_balance)
    except Exception as e:
        print(e)
        time.sleep(1)
#print(Day)
#print(Price)
#print(ask_amount)
#print(bid_amount)
#print(VG_Price_End/VG_Price_Start*100)
#print(k_ratio)
#print(Asset_End / Asset_Start * 100)
#print(Buy_count)
#f.close()
