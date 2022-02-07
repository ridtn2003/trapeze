# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 20:50:04 2022

Time Marketing
@author: ksoo
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 22:59:22 2022

@author: ksoo
"""



## 변수
import numpy as np
import pyupbit

ticker = "KRW-BTC"
Alpha_Array = list(range(0, 64))
Profit_Array = list(range(0, 64))
max_Array = list(range(0,8))
Total_Asset = 100000
interval_value = "minute30"
sample_count = 2 * 24 * 365 
Value_bit = 48
jj = 0
for i in list(range(0, 64)):
    Alpha_Array[jj] = np.random.randint(0,2**24) * np.random.randint(0,2**24) + np.random.randint(0,2)
    jj = jj +1
t=0
df_test = pyupbit.get_ohlcv(ticker, count=sample_count, interval = interval_value)

#while True:                  ## L1 유전적 세대 수
for i in list(range(0,1000)):
    t = t+1
    t_str = "***********************t value is " + str(t) + "*********************************"
    print(t_str)
   
    jj=0    
    for i in list(range(0, 64)):            ### L2 Alpha Array 수 Case 64
    
        a=list(range(0,48))                 ### Alpha Array 동안 돌연변이 시험
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
        k_ratio = a[0] * 2**0 + a[1] * 2**1+ a[2] * 2**2+ a[3] * 2**3+ a[4] * 2**4+ a[5] * 2**5+ a[6] * 2**6+ a[7] * 2**7+ a[8] * 2**8+ a[9] * 2**9+ a[10] * 2**10+ a[11] * 2**11+ a[12] * 2**12+ a[13] * 2**13+ a[14] * 2**14+ a[15] * 2**15+ a[16] * 2**16+ a[17] * 2**17+ a[18] * 2**18+ a[19] * 2**19+ a[20] * 2**20+ a[21] * 2**21+ a[22] * 2**22+ a[23] * 2**23+ a[24] * 2**24+ a[25] * 2**25+ a[26] * 2**26+ a[27] * 2**27+ a[28] * 2**28+ a[29] * 2**29+ a[30] * 2**30+ a[31] * 2**31+ a[32] * 2**32+ a[33] * 2**33+ a[34] * 2**34+ a[35] * 2**35+ a[36] * 2**36+ a[37] * 2**37+ a[38] * 2**38+ a[39] * 2**39+ a[40] * 2**40+ a[41] * 2**41+ a[42] * 2**42+ a[43] * 2**43+ a[44] * 2**44+ a[45] * 2**45+ a[46] * 2**46+ a[47] * 2**47
        k = 0
        buy_flag = 1
        sell_flag = 0
        KRW = 100000
        BTC = 0
        for i in range(0,len(df_test)-1):
             #if(i%30 ==  0):
            #print(k)
            Price = df_test.iloc[i]['open']
            KRW_before = KRW
            BTC_before = BTC
            if(k==48):
                k=0
            if(a[k] == 1 and buy_flag == 1):
                buy_flag = 0
                sell_flag = 1
                KRW = KRW_before * 0.1
                BTC = BTC_before + (KRW_before*0.9) / Price *(1-0.0005)
            elif(a[k] == 0 and sell_flag == 1):
                buy_flag = 1
                sell_flag = 0
                KRW = KRW_before + BTC_before * 0.9 * Price *(1-0.0005)
                BTC = BTC_before * 0.1
            k=k+1
        Profit_Array[jj] = KRW + BTC * Price
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
        Value_bit = Value_bit / 2
        ## + mutant
        Alpha_Array[16] = Alpha_Array[0] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[17] = Alpha_Array[1] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[18] = Alpha_Array[2]  + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[19] = Alpha_Array[3] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[20] = Alpha_Array[4] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[21] = Alpha_Array[5] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[22] = Alpha_Array[6] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[23] = Alpha_Array[7] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[24] = Alpha_Array[8] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[25] = Alpha_Array[9] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[26] = Alpha_Array[10] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[27] = Alpha_Array[11] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[28] = Alpha_Array[12] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[29] = Alpha_Array[13] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[30] = Alpha_Array[14] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[31] = Alpha_Array[15] + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        ## - Mutant
        Alpha_Array[32] = Alpha_Array[0] - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[33] = Alpha_Array[1]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[34] = Alpha_Array[2]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[35] = Alpha_Array[3]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[36] = Alpha_Array[4]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[37] = Alpha_Array[5]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[38] = Alpha_Array[6]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[39] = Alpha_Array[7]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[40] = Alpha_Array[8]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[41] = Alpha_Array[9]  - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[42] = Alpha_Array[10] - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[43] = Alpha_Array[11] - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[44] = Alpha_Array[12] - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[45] = Alpha_Array[13] - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[46] = Alpha_Array[14] - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        Alpha_Array[47] = Alpha_Array[15] - 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) 
        ## X2 +Mutant
        Alpha_Array[48] = Alpha_Array[0]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        Alpha_Array[49] = Alpha_Array[1]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        Alpha_Array[50] = Alpha_Array[2]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        Alpha_Array[51] = Alpha_Array[3]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        Alpha_Array[52] = Alpha_Array[4]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        Alpha_Array[53] = Alpha_Array[5]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        Alpha_Array[54] = Alpha_Array[6]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        Alpha_Array[55] = Alpha_Array[7]  + 2**np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) * np.random.randint(0,Value_bit) + 2**np.random.randint(0,Value_bit) 
        ## X2 -Mutant
        Alpha_Array[56] = np.random.randint(0,2**Value_bit) * np.random.randint(0,2**Value_bit) 
        Alpha_Array[57] = np.random.randint(0,2**Value_bit) * np.random.randint(0,2**Value_bit) 
        Alpha_Array[58] = np.random.randint(0,2**Value_bit) * np.random.randint(0,2**Value_bit) 
        Alpha_Array[59] = np.random.randint(0,2**Value_bit) * np.random.randint(0,2**Value_bit) 
        Alpha_Array[60] = np.random.randint(0,2**Value_bit) * np.random.randint(0,2**Value_bit) 
        Alpha_Array[61] = np.random.randint(0,2**Value_bit) * np.random.randint(0,2**Value_bit) 
        Alpha_Array[62] = np.random.randint(0,2**Value_bit) * np.random.randint(0,2**Value_bit) 
        Alpha_Array[63] = Alpha_Array[0]
        Value_bit = Value_bit *  2
    
    Alpha_Array_tmp = Alpha_Array[0]
    k=0
    for i in a:
        a[k] = 0 
        k=k+1
    k=0
    while(Alpha_Array_tmp != 0):            ## 2진 분할
        #a.insert(0,Alpha_Array_tmp%2)
        a[k] = Alpha_Array_tmp%2
        Alpha_Array_tmp = Alpha_Array_tmp//2
        #print(Alpha_Array_tmp)
        k= k+1
    
    k_ratio = a[0] * 2**0 + a[1] * 2**1+ a[2] * 2**2+ a[3] * 2**3+ a[4] * 2**4+ a[5] * 2**5+ a[6] * 2**6+ a[7] * 2**7+ a[8] * 2**8+ a[9] * 2**9+ a[10] * 2**10+ a[11] * 2**11+ a[12] * 2**12+ a[13] * 2**13+ a[14] * 2**14+ a[15] * 2**15+ a[16] * 2**16+ a[17] * 2**17+ a[18] * 2**18+ a[19] * 2**19+ a[20] * 2**20+ a[21] * 2**21+ a[22] * 2**22+ a[23] * 2**23+ a[24] * 2**24+ a[25] * 2**25+ a[26] * 2**26+ a[27] * 2**27+ a[28] * 2**28+ a[29] * 2**29+ a[30] * 2**30+ a[31] * 2**31+ a[32] * 2**32+ a[33] * 2**33+ a[34] * 2**34+ a[35] * 2**35+ a[36] * 2**36+ a[37] * 2**37+ a[38] * 2**38+ a[39] * 2**39+ a[40] * 2**40+ a[41] * 2**41+ a[42] * 2**42+ a[43] * 2**43+ a[44] * 2**44+ a[45] * 2**45+ a[46] * 2**46+ a[47] * 2**47
    print(max_value)
    

    #print(VG_Price_End/VG_Price_Start*100)
    #print(Asset_End / Asset_Start * 100)
    #print(Buy_count)
    #f.close()
