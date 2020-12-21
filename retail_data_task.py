# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 23:28:19 2020

@author: Oscar
"""
import pandas as pd 
import numpy as np

data = pd.read_csv("C:/Users/Oscar/Desktop/UOxford/Retail Hands-on Exercise - Beacon dataset/beacon_data.csv", sep = ';')
data.head()


### Remove unuseful columns
data = data.drop("merchant_id",axis = 1)
data = data.drop("dongle_id",axis = 1)


### check if columns has na values ####

for column in data:
    print(column +' '+ str(data[column].isnull().values.any()) +' '+str(sum(data[column].isnull())/len(data)))

### check dates and signal type #####

data_noNA_dates = data[["entry_date","exit_date"]].dropna()

cases = 0
for i in range(0,len(data_noNA_dates)):
    #cases = 0
    if data_noNA_dates["entry_date"].iloc[i] == data_noNA_dates["exit_date"].iloc[i]:
        cases += 1
    else:
        cases.append(0)
cases/len(data_noNA_dates) ## the exit date h
        
data_noNA_dates.groupby()