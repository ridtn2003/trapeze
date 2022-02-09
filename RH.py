# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 23:48:09 2022

@author: ksoo
Riding Horse
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
count_value = 30
tickers=pyupbit.get_tickers()
KRW_All_tickers = []
for obj in tickers:
    if(obj[0:3] == "KRW"):
        KRW_All_tickers.append(obj)

max_ticker_origin = "KRW-BTC"
max_ticker = "KRW-BTC"
        
while True:
    len(KRW_All_tickers)
    k=0
    profit = 1
    profit_before = 1
    for i in KRW_All_tickers:
        df_test = pyupbit.get_ohlcv(i, count=count_value, interval = "minute1")
        if(str(type(df_test)) == "<class 'pandas.core.frame.DataFrame'>"):
            df_test_origin = df_test
            profit = df_test_origin['open'][count_value-1]/df_test_origin['open'][0]
            #print(profit)
            if(profit > profit_before):
                profit_before = profit
                max_ticker = i
                print(i)   
                #print(profit)
    
    if(max_ticker_origin != max_ticker):
            upbit.sell_market_order(max_ticker_origin,get_balance(max_ticker_origin[4::]))
            upbit.buy_market_order(max_ticker, get_balance("KRW")*0.9)
            max_ticker_origin = max_ticker     
    time.sleep(1800)
    
    

#for i in list(range(0,4)):
#    max_Array[i] = (Alpha_Array[max_list[i]]) 
        
    #print(k)
    #k=k+1
