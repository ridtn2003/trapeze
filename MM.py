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
ticker = "KRW-JST"
df_test = pyupbit.get_ohlcv(ticker, count=1000, interval = "minute1")

#print(ask_price)
#print(bid_price)

k=0
bid_flag = 0
buy_flag = 0
sell_flag = 1



KRW = get_balance("KRW")

BTC = get_balance("JST") * float(pyupbit.get_current_price(ticker))
ksoo_balance_Start = KRW + BTC
VG_Price_Start = pyupbit.get_current_price("KRW-JST")

while True:
    orderbook = pyupbit.get_orderbook(ticker, limit_info =True)
    ask_price_order = orderbook[0]['orderbook_units'][1]['ask_price']
    bid_price_order = orderbook[0]['orderbook_units'][1]['bid_price']
    ask_price_order_0 = orderbook[0]['orderbook_units'][2]['ask_price']
    bid_price_order_0 = orderbook[0]['orderbook_units'][2]['bid_price']
    KRW = get_balance("KRW")
    BTC = get_balance("JST") * float(pyupbit.get_current_price(ticker))
    BTC_Value = get_balance("JST")
    if(buy_flag == 0):
        if(bid_flag ==  0):         ## 사려는 가격 책정
            bid_price = bid_price_order
            buy_uuid = upbit.buy_limit_order(ticker, bid_price, int(KRW*0.9/bid_price))
            print("buy")
            bid_flag = 1
        elif(bid_flag == 1):        ## 살 떄 까지 대기
            if(upbit.get_order("KRW-JST") == []):
                buy_flag = 1
                sell_flag = 0
                ask_flag = 0
            elif(bid_price <=  bid_price_order_0 ):
                bid_price = bid_price_order
                #order = upbit.get_order(ticker)
                upbit.cancel_order(buy_uuid['uuid'])
                print("cancel")
                KRW = get_balance("KRW")
                buy_uuid = upbit.buy_limit_order(ticker, bid_price, int(KRW*0.9/bid_price))
                time.sleep(1)
                print("buy")
                time.sleep(1)
    if(sell_flag == 0):
        if(ask_flag == 0):
            ask_price = ask_price_order
            sell_uuid = upbit.sell_limit_order(ticker, ask_price, int(BTC_Value))
            print("sell")
            ask_flag = 1    
        elif(ask_flag == 1):
            if(upbit.get_order("KRW-JST") == []):
                buy_flag = 0
                sell_flag = 1
                bid_flag = 0
                ksoo_balance = get_balance('KRW') + get_balance('JST') * pyupbit.get_current_price(ticker) 
                ksoo_balance_value = get_balance('KRW') + get_balance('JST') * pyupbit.get_current_price(ticker) 
                ksoo_balance = 'ksoo balance = ' + str(ksoo_balance)
                print("Profit of MM")
                print(ksoo_balance_value/ksoo_balance_Start*100)
                print("Profit of Nature")
                print(pyupbit.get_current_price(ticker)/VG_Price_Start*100)
                print(ksoo_balance)
            elif(ask_price >= ask_price_order_0 ):
                ask_price = ask_price_order
                #order = upbit.get_order(ticker)
                upbit.cancel_order(sell_uuid['uuid'])
                print("cancel")
                BTC_Value = get_balance("JST")
                sell_uuid = upbit.sell_limit_order(ticker, ask_price, int(BTC_Value))
                print("sell")
                time.sleep(1)

    time.sleep(1)

    
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
