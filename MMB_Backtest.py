# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 19:42:04 2022

Market Making
@author: ksoo
"""

# Function
# 0. 초기 환경
# 1. 주요 변수 설정
# 2. 실행문


# Function
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

# 0. 초기 환경
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
    count_value = 60 * 24
    orderbook = pyupbit.get_orderbook(ticker, limit_info =True)
    #tickers=pyupbit.get_tickers()
    #ask_price = orderbook[0]['orderbook_units'][0]['ask_price']
    #bid_price = orderbook[0]['orderbook_units'][0]['bid_price']
    Alpha_Array = list(range(0, 64))
    Profit_Array = list(range(0, 64))
    max_Array = list(range(0,4))
    Value_bit = 22
    jj = 0


# 1. 주요 변수 설정
    for i in list(range(0, 64)):
        time_box = 10
        range_box = 5
        tic_buy = 0
        tic_sell = 2
        Alpha_Array_tmp = time_box + range_box * 2**10 + tic_buy * 2**14 + tic_sell * 2**18
        Alpha_Array[jj] = Alpha_Array_tmp
        jj = jj +1
    jj=0
    for i in list(range(0, 64)):
        Profit_Array[jj] = 0
        jj = jj +1
    t=0
    df_test = pyupbit.get_ohlcv(ticker, count= count_value, interval = "minute1")


# 2. 실행문
    while True:                  ## L1 유전적 세대 수
        #for i in list(range(0,2)):
        # 2.1 초기 변수 설정
        if df_test is None : continue
        t = t+1
        t_str = "***********************t value is " + str(t) + "*********************************"
        print(t_str)
        jj=0    

        # 2.2 메인 알고리즘
        for i in list(range(0, 64)):            ### 메인 알고리즘
            a=list(range(0,Value_bit*2))                 ### Alpha Array 동안 돌연변이 시험 
            k=0        
            for i in a:
                a[k] = 0 
                k=k+1
            if(-1 < Alpha_Array[jj] < 2**Value_bit):
                Alpha_Array_tmp = Alpha_Array[jj]
            else:
                Alpha_Array_tmp = Alpha_Array[0]
            #Alpha_Array_tmp = Alpha_Array[jj]
            k=0
            while(Alpha_Array_tmp != 0):
                #a.insert(0,Alpha_Array_tmp%2)
                a[k] = Alpha_Array_tmp%2
                Alpha_Array_tmp = Alpha_Array_tmp//2
                #print(Alpha_Array_tmp)
                k= k+1
                
            time_box = a[0] * 2**0 + a[1] * 2**1+ a[2] * 2**2+ a[3] * 2**3+ a[4] * 2**4+ a[5] * 2**5 
            if(time_box == 0):
                time_box = 1
            range_box = a[10] * 2**0 + a[11] * 2**1 + a[12] * 2**2 + a[13] * 2**3 ## 10~13 
            tic_buy = a[14] * 2**0 + a[15] * 2**1 + a[16] * 2**2 + a[17] * 2**3 ## 14~17
            tic_sell = a[18] * 2**0 + a[19] * 2**1 + a[20] * 2**2 + a[21] * 2**3 ## 18~21
            #count_value = 6 * 24 * (a[22] * 2**0 + a[23] + 2**1+ a[24] * 2**2 + a[25] * 2**3 + a[26] *2**4)
            time_box = int(time_box)
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
            price_init = df_test.iloc[0]['open'] - 0.5
            price_current = price_init
            VG_Price_Start = price_init
            price_buy = price_current - 0.5
            price_sell = price_current + 0.5
            box_flag = 0
            Total_Box = list(range(0,time_box))
            Sum_Box = 0
            box_i=0
            for j in list(range(0, count_value )):
                price_currnet_before = price_current
                price_buy_before = price_buy
                price_sell_before = price_sell
                price_current = df_test.iloc[j]['open'] - 0.5
                price_buy = price_current - 0.5
                price_sell = price_current + 0.5
                Avg_Box = price_current
                ## Box권 설정
                #print(price_current)
                Total_Box[box_i] =  df_test.iloc[j]['open'] - 0.5
                Sum_Box = Sum_Box + Total_Box[box_i]
                box_i = box_i + 1
                if(box_i == time_box):
                    box_i = 0
                if(j>time_box):
                    Avg_Box = round(Sum_Box / time_box)
                    max_list = sorted(range(len(Total_Box)), key=lambda g: Total_Box[g])[-1 * time_box:]
                    min_box = Total_Box[max_list[0]]
                    max_box = Total_Box[max_list[-1]]
                    if(j > 10):
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
                    if(sell_flag == 0):
                        Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (price_current - bid_price)) * (1-0.001)
                        #print("unbox")
                    ##flag init
                    buy_flag = 0
                    bid_flag = 0
                    sell_flag = 1
                    ask_flag = 1
            
                if(box_flag == 1): 
                    ## 구매 Module
                    if(buy_flag == 0):
                        if(bid_flag ==  0 and price_init != price_current):         ## 사려는 가격 책
                            price_init = 0
                            #bid_price = price_buy - tic_buy
                            if(Avg_Box - tic_buy <= price_buy):
                                bid_price = Avg_Box - tic_buy
                                bid_flag = 1
                            elif(Avg_Box - tic_buy > price_buy):
                                bid_price = price_buy - tic_buy
                                bid_flag = 1
                            #print(bid_price)
                        elif(bid_flag == 1):        ## 살 떄 까지 대기
                            if(bid_price >= price_current ):
                                #print("buy")
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
                            elif(Avg_Box + tic_sell < price_sell):
                                ask_price = price_sell + tic_sell                
                            ask_flag = 1    
                        elif(ask_flag == 1):
                            if(ask_price <= price_current):
                                #print("sell")
                                bid_flag = 0         
                                Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (ask_price - bid_price)) * (1-0.001)
                                #print(Total_Asset)
                                #print(bid_price)
                                #print(ask_price)
                                sell_flag = 1
                                buy_flag = 0
                                ask_flag = 0
                                buy_count = buy_count + 1
                #print(price_current)
                #print(Avg_Box)
            #print(Total_Asset)
            if(sell_flag == 0):
                Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (price_current - bid_price)) * (1-0.001)
            VG_Price_End = price_current
            Asset_End = Total_Asset
            Asset_Start = 100000
            Profit_Standard = (Asset_End / Asset_Start * 100) / (VG_Price_End/VG_Price_Start*100) 
            if(buy_count == 0 ):
                Profit_Standard = 0
            Profit_Standard_str = "profit_Standard " + str(Profit_Standard)
            Profit_Array[jj] = Profit_Standard
            if(buy_count != 0):
                print(Profit_Standard_str)
                print(Alpha_Array[jj])
                print(buy_count)
            else:
                print("nothing")
            
            #print(jj)
            jj = jj + 1
        max_list = sorted(range(len(Profit_Array)), key=lambda g: Profit_Array[g])[-4:] ## L2 최대값 산출 및 정리
        max_list = max_list[::-1]
        max_value = []
        
        # 2.3 후처리
        for i in list(range(0,4)):
            max_value.append(Profit_Array[max_list[i]])
        
        for i in list(range(0,4)):
            max_Array[i] = (Alpha_Array[max_list[i]]) 
        
        for i in list(range(0, 1)):             ## 유전적 알고리즘 셋팅
            Alpha_Array[0]  = int(max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2))
            Alpha_Array[1]  = int(max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2))
            Alpha_Array[2]  = int(max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2))
            Alpha_Array[3]  = int(max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2))
            Alpha_Array[4]  = int(max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2))
            Alpha_Array[5]  = int(max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2))
            Alpha_Array[6]  = int(max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2))
            Alpha_Array[7]  = int(max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2))
            Alpha_Array[8]  = int(max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2))
            Alpha_Array[9]  = int(max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2))
            Alpha_Array[10] = int(max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2))
            Alpha_Array[11] = int(max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2))
            Alpha_Array[12] = int(max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2))
            Alpha_Array[13] = int(max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2))
            Alpha_Array[14] = int(max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2))
            Alpha_Array[15] = int(max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2))
            ## + mutant
            Alpha_Array[16] = int(Alpha_Array[0] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[17] = int(Alpha_Array[1] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[18] = int(Alpha_Array[2]  + 2**np.random.randint(0,Value_bit))
            Alpha_Array[19] = int(Alpha_Array[3] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[20] = int(Alpha_Array[4] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[21] = int(Alpha_Array[5] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[22] = int(Alpha_Array[6] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[23] = int(Alpha_Array[7] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[24] = int(Alpha_Array[8] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[25] = int(Alpha_Array[9] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[26] = int(Alpha_Array[10] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[27] = int(Alpha_Array[11] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[28] = int(Alpha_Array[12] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[29] = int(Alpha_Array[13] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[30] = int(Alpha_Array[14] + 2**np.random.randint(0,Value_bit))
            Alpha_Array[31] = int(Alpha_Array[15] + 2**np.random.randint(0,Value_bit))
            ## - Mutant
            Alpha_Array[32] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[33] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[34] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[35] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[36] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[37] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[38] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[39] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[40] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[41] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[42] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[43] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[44] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[45] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[46] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[47] = int(np.random.randint(0,2**Value_bit))
            ## X2 +Mutant
            Alpha_Array[48] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[49] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[50] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[51] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[52] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[53] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[54] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[55] = int(np.random.randint(0,2**Value_bit))
            ## X2 -Mutant
            Alpha_Array[56] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[57] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[58] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[59] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[60] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[61] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[62] = int(np.random.randint(0,2**Value_bit))
            Alpha_Array[63] = int(np.random.randint(0,2**Value_bit))

        Alpha_Array_tmp = Alpha_Array[0]
        k=0    
        for i in a:
            a[k] = 0 
            k=k+1

        k=0
        while(Alpha_Array_tmp != 0):            ## 10진수 --> 2진수
            #a.insert(0,Alpha_Array_tmp%2)
            a[k] = Alpha_Array_tmp%2
            Alpha_Array_tmp = Alpha_Array_tmp//2
            #print(Alpha_Array_tmp)
            k= k+1
        
        if(time_box == 0):
            time_box = 1
        
        # 2.4 결과 값 정리 
        time_box = a[0] * 2**0 + a[1] * 2**1+ a[2] * 2**2+ a[3] * 2**3+ a[4] * 2**4+ a[5] * 2**5 
        range_box = a[10] * 2**0 + a[11] * 2**1+ a[12] * 2**2 + a[13] * 2**3 ## 10~13 
        tic_buy = a[14] * 2**0 + a[15] * 2**1 + a[16] * 2**2 + a[17] * 2**3 ## 14~17
        tic_sell = a[18] * 2**0 + a[19] * 2**1+ a[20] * 2**2 + a[21] * 2**3 ## 18~21
        
        print("time_box")
        print(time_box)
        print("range_box")
        print(range_box)
        print("tic_buy")
        print(tic_buy)
        print("tic_sell")
        print(tic_sell)
        print(count_value)
        print(Alpha_Array_tmp)

        
    if(sell_flag == 0):
        Total_Asset = (Total_Asset + Total_Asset / df_test.iloc[i]['open'] * (price_current - bid_price)) * (1-0.001)
    print(Total_Asset)







