# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 19:42:04 2022

Market Making
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

#tickers=pyupbit.get_tickers()
#print(tickers)\
ticker = "KRW-DOGE"
df_test = pyupbit.get_ohlcv(ticker, count=20000, interval = "minute1")
orderbook = pyupbit.get_orderbook(ticker, limit_info =True)
ask_price = orderbook[0]['orderbook_units'][0]['ask_price']
bid_price = orderbook[0]['orderbook_units'][0]['bid_price']

#print(ask_price)
#print(bid_price)

k=0
bid_flag = 0
buy_flag = 0
sell_flag = 1
Total_Asset = 100000
for i in list(range(0,20000)):
    #print(i)
    if(buy_flag == 0):
        if(bid_flag ==  0):         ## 사려는 가격 책정
            bid_price = df_test.iloc[i]['open'] - 1
            bid_flag = 1            
        elif(bid_flag == 1):        ## 살 떄 까지 대기
            if(bid_price == df_test.iloc[i]['open']):
                buy_flag = 1
                sell_flag = 0
                ask_flag = 0
            elif(bid_price != df_test.iloc[i]['open'] -1 ):
                bid_price = df_test.iloc[i]['open'] + 1
    if(sell_flag == 0):
        if(ask_flag == 0):
            ask_price = df_test.iloc[i]['open'] + 1
            ask_flag = 1    
        elif(ask_flag == 1):
            if(ask_price == df_test.iloc[i]['open']):
                Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (ask_price - bid_price)) * (1-0.001)
                print(ask_price)
                print(bid_price)
                sell_flag = 1
                buy_flag = 0
                ask_flag = 0
            elif(ask_price != df_test.iloc[i]['open'] + 1 ):
                ask_price = df_test.iloc[i]['open'] + 1
    print(Total_Asset)

    
"""    
if(df_test.iloc[i] == bid_price and ):  ## BTC 사라
    #if(bid_amount*k_ratio < ask_amount and Sell_Flag == 1):  ## BTC 사라
    longevity_buy = longevity_buy + 1
    #print(longevity_buy)
    if(longevity_buy == longevity_ratio_buy):
        Sell_Flag = 0
        Buy_Flag = 1
        Buy_count = Buy_count + 1
        #print("Buy")
        BTC_before = BTC
        KRW_before = KRW
        BTC = BTC_before + (KRW_before*0.9) / Price *(1-0.0005)
        KRW = KRW_before *0.1
        longevity_buy = 0
elif(bid_amount * k_ratio < ask_amount and Buy_Flag == 1):  ## BTC 팔아라
#elif(bid_amount > k_ratio * ask_amount and Buy_Flag == 1):  ## BTC 팔아라
    longevity_sell = longevity_sell + 1
    if(longevity_sell == longevity_ratio_sell):
        Sell_Flag = 1
        Buy_Flag = 0
        Sell_count = Sell_count + 1
        #print("Sell")
        BTC_before = BTC
        KRW_before = KRW
        KRW = KRW_before + BTC_before*0.9 * Price * (1-0.0005)
        BTC = BTC_before * 0.1     
        longevity_sell = 0
"""
    #print("fuck")
    #df_test[]
