# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 22:59:22 2022

@author: ksoo
"""



## 변수
import numpy as np

Alpha_Array = list(range(0, 64))
Profit_Array = list(range(0, 64))
max_Array = list(range(0,8))
Value_bit = 14
jj = 0
for i in list(range(0, 64)):
    Alpha_Array[jj] = np.random.randint(0,2**14)
    jj = jj +1

for t in list(range(0,2)):                  ## L1 유전적 세대 수
    t_str = "***********************t value is " + str(t) + "*********************************"
    print(t_str)
    jj=0    
    for i in list(range(0, 64)):            ### L2 Alpha Array 수 Case 64
    
        a=list(range(0,15))                 ### Alpha Array 동안 돌연변이 시험
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
        ##split 변수    
        k_ratio = a[0] * 2**0 + a[1] * 2**1+ a[2] * 2**2+ a[3] * 2**3+ a[4] * 2**4+ a[5] * 2**5 ## 0~5
        longevity_split =  a[6] * 2**0 + a[7] * 2**1+ a[8] * 2**2+ a[9] * 2**3+ a[10] * 2**4+ a[11] * 2**5    ## 6~11
        cnt_split  = a[12] * 2**0 + a[13] * 2**1+ a[14] * 2**2   #12~14
        #while(k_ratio < 50):    ## change
        with open("AB_Test.log",'r') as infile:
            data = infile.read()
        my_list = data.splitlines()
        #f=open("AB_0121.log",'r')
    #    k_ratio = k_ratio+1       ##change
        cnt = 0
        cnt_ratio = 4 + 4 * 60 * 60 * 24 * cnt_split  ## change
        #cnt_ratio= 102436  ## change
        longevity_buy = 0
        longevity_sell = 0
        longevity_ratio_buy = longevity_split   ## change
        longevity_ratio_sell = longevity_split  ## change
        Asset_Start = 100000
        Asset_End = 100000
        KRW = 100000
        BTC = 0
        KRW_before = 100000
        BTC_before = 0
        Buy_Flag = 0
        Sell_Flag = 1
        Buy_count = 0
        Sell_count = 0
    
        #while True:
        while cnt < cnt_ratio:                          ## Case 1               
            line = my_list[int(cnt-cnt_ratio)]
            cnt = cnt+1
            #line = f.readline()
            if not line: break
            line = line.strip('\n')
        #    print(line)
            if(cnt % 4 == 1):   ## 날짜
                Day = line
            if(cnt % 4 == 2):   ## 가격
                Price = float(line)
            if(cnt % 4 == 3):   ## 매도 호가
                ask_amount = float(line)
            if(cnt % 4 == 0):   ## 매수 호가
                bid_amount = float(line)
            if(cnt > 4 and cnt % 4 == 0):
                if(bid_amount > k_ratio * ask_amount and Sell_Flag == 1):  ## BTC 사라
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
                else:
                    longevity_buy = 0
                    longevity_sell = 0
                    
                Asset_End = KRW + BTC * Price   ## 자산 총액
                #print(Day)
                #print(Price)
                #print(Asset_End)
                #print(KRW)
                #print(BTC)
                #print(Price)
            if(cnt ==2):
                VG_Price_Start = float(line)   ## 평가 기준 시작점
            if(cnt % 4 == 2):
                VG_Price_End = float(line)   ## 평가 기준 끝점
        #print(Day)
        #print(Price)
        #print(ask_amount)
        #print(bid_amount)
        #print(Alpha_Array)
        k_ratio_str = "k_ratio " + str(k_ratio)
        print(k_ratio_str)
        longevity_split_str = "longevity " + str(longevity_split)
        print(longevity_split_str)
        cnt_split_str = "cnt " + str(cnt_split)
        print(cnt_split_str)
        Profit_Standard = (Asset_End / Asset_Start * 100) / (VG_Price_End/VG_Price_Start*100) 
        Profit_Standard_str = "profit_Standard " + str(Profit_Standard)
        Profit_Array[jj] = Profit_Standard
        print(Profit_Standard_str)
        jj = jj + 1
    max_list = sorted(range(len(Profit_Array)), key=lambda g: Profit_Array[g])[-4:] ## L2 최대값 산출 및 정리
    max_list = max_list[::-1]
    max_value = []
    
    for i in list(range(0,4)):
        max_value.append(Profit_Array[max_list[i]])
    
    for i in list(range(0,4)):
        max_Array[i] = (Alpha_Array[max_list[i]]) 
    
    for i in list(range(0, 1)):             ## 유전적 알고리즘을 위한 정리
        Alpha_Array[0]  = max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2)            
        Alpha_Array[1]  = max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2)            
        Alpha_Array[2]  = max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2)            
        Alpha_Array[3]  = max_Array[0] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2)            
        Alpha_Array[4]  = max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2)            
        Alpha_Array[5]  = max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2)            
        Alpha_Array[6]  = max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2)            
        Alpha_Array[7]  = max_Array[1] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2)            
        Alpha_Array[8]  = max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2)            
        Alpha_Array[9]  = max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2)            
        Alpha_Array[10] = max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2)           
        Alpha_Array[11] = max_Array[2] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2)           
        Alpha_Array[12] = max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[0] % 2**(Value_bit/2)           
        Alpha_Array[13] = max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[1] % 2**(Value_bit/2)           
        Alpha_Array[14] = max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[2] % 2**(Value_bit/2)           
        Alpha_Array[15] = max_Array[3] // 2**(Value_bit/2) * 2**(Value_bit/2) + max_Array[3] % 2**(Value_bit/2)  
        ## + mutant
        Alpha_Array[16] = Alpha_Array[0] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[17] = Alpha_Array[1] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[18] = Alpha_Array[2]  + 2**np.random.randint(0,Value_bit)
        Alpha_Array[19] = Alpha_Array[3] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[20] = Alpha_Array[4] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[21] = Alpha_Array[5] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[22] = Alpha_Array[6] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[23] = Alpha_Array[7] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[24] = Alpha_Array[8] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[25] = Alpha_Array[9] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[26] = Alpha_Array[10] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[27] = Alpha_Array[11] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[28] = Alpha_Array[12] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[29] = Alpha_Array[13] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[30] = Alpha_Array[14] + 2**np.random.randint(0,Value_bit)
        Alpha_Array[31] = Alpha_Array[15] + 2**np.random.randint(0,Value_bit)
        ## - Mutant
        Alpha_Array[32] = Alpha_Array[0] - 2**np.random.randint(0,Value_bit)
        Alpha_Array[33] = Alpha_Array[1]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[34] = Alpha_Array[2]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[35] = Alpha_Array[3]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[36] = Alpha_Array[4]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[37] = Alpha_Array[5]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[38] = Alpha_Array[6]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[39] = Alpha_Array[7]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[40] = Alpha_Array[8]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[41] = Alpha_Array[9]  - 2**np.random.randint(0,Value_bit)
        Alpha_Array[42] = Alpha_Array[10] - 2**np.random.randint(0,Value_bit)
        Alpha_Array[43] = Alpha_Array[11] - 2**np.random.randint(0,Value_bit)
        Alpha_Array[44] = Alpha_Array[12] - 2**np.random.randint(0,Value_bit)
        Alpha_Array[45] = Alpha_Array[13] - 2**np.random.randint(0,Value_bit)
        Alpha_Array[46] = Alpha_Array[14] - 2**np.random.randint(0,Value_bit)
        Alpha_Array[47] = Alpha_Array[15] - 2**np.random.randint(0,Value_bit)
        ## X2 +Mutant
        Alpha_Array[48] = Alpha_Array[0]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        Alpha_Array[49] = Alpha_Array[1]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        Alpha_Array[50] = Alpha_Array[2]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        Alpha_Array[51] = Alpha_Array[3]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        Alpha_Array[52] = Alpha_Array[4]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        Alpha_Array[53] = Alpha_Array[5]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        Alpha_Array[54] = Alpha_Array[6]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        Alpha_Array[55] = Alpha_Array[7]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit)
        ## X2 -Mutant
        Alpha_Array[56] = np.random.randint(0,2**Value_bit)
        Alpha_Array[57] = np.random.randint(0,2**Value_bit)
        Alpha_Array[58] = np.random.randint(0,2**Value_bit)
        Alpha_Array[59] = np.random.randint(0,2**Value_bit)
        Alpha_Array[60] = np.random.randint(0,2**Value_bit)
        Alpha_Array[61] = np.random.randint(0,2**Value_bit)
        Alpha_Array[62] = np.random.randint(0,2**Value_bit)
        Alpha_Array[63] = np.random.randint(0,2**Value_bit)
    
    Alpha_Array_tmp = Alpha_Array[0]
    k=0
    while(Alpha_Array_tmp != 0):            ## 2진 분할
        #a.insert(0,Alpha_Array_tmp%2)
        a[k] = Alpha_Array_tmp%2
        Alpha_Array_tmp = Alpha_Array_tmp//2
        #print(Alpha_Array_tmp)
        k= k+1
        
    k_ratio = a[0] * 2**0 + a[1] * 2**1+ a[2] * 2**2+ a[3] * 2**3+ a[4] * 2**4+ a[5] * 2**5 ## 0~5
    longevity_split =  a[6] * 2**0 + a[7] * 2**1+ a[8] * 2**2+ a[9] * 2**3+ a[10] * 2**4+ a[11] * 2**5    ## 6~11
    cnt_split  = a[12] * 2**0 + a[13] * 2**1+ a[14] * 2**2   #12~14
    f = open("k.log", 'w')
    f.write(str(k_ratio))
    f.write(str(longevity_split))
    f.write(str(cnt_split))
    f.close()

    #print(VG_Price_End/VG_Price_Start*100)
    #print(Asset_End / Asset_Start * 100)
    #print(Buy_count)
    #f.close()
