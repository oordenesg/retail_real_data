# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 23:28:19 2020

@author: Oscar
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("C:/Users/Oscar/Desktop/UOxford/Beacon dataset/beacon_data.csv", sep = ';')
data.head()

# SVM: Using multiple features (location, distance, RSSI, length of stay etc.), 
# predict for a particular application (vendor id) the number of sale in a day 
# is above a contain level.


### 1. Check if the columns have NA values #### 

for column in data:
    print(column +' '+ str(data[column].isnull().values.any()) +' '+str(sum(data[column].isnull())/len(data)))

### The column exit_date has the same value in the column entry_date

### 2. Check the columns signal_type, entry_date and exit_date  
#       when entry_date and exit_date are the same. In this case signal
#       signal_type should be equal 4
# First, I am creating a new dataset with 3 columns    
data_noNA_dates = data[["signal_type","entry_date","exit_date"]].dropna()

#Now I can check if entry_date = exit_date when signal = 4
cases = 0
for i in range(0,len(data_noNA_dates)):
    #cases = 0
    if data_noNA_dates["entry_date"].iloc[i] == data_noNA_dates["exit_date"].iloc[i] and data_noNA_dates["signal_type"].iloc[i] ==4:
        cases += 1
    else:
        cases.append(0);
cases/len(data_noNA_dates) ## output is equal to 1. With this I can confirm that the column exit_date is useless


## Remove unuseful columns
data = data.drop("merchant_id",axis = 1) # unique ID
data = data.drop("dongle_id",axis = 1) # unique ID
data = data.drop("exit_date",axis = 1) # same values 


### 3. Duplicated values using columns from vendor_id 
# I removed all the repeated values that I found

duplicated_values = data.iloc[:,2:len(data.columns)].duplicated()
data = data[duplicated_values == False]


### Optional. Find the transaccion with more rows
### movement unique per user_id 
data[["subscriber_id","gtid"]].groupby(by = "subscriber_id").nunique()
data[["subscriber_id","gtid"]].groupby(by = "subscriber_id").count()



#### 4. Analsing the RSSI column.  
# RSSI in some cases is zero for some "immediate" signal. 
# This situation is similar for the signal "far". This column has values > 0

# Check the data 
data.boxplot(column = "rssi", by = "proximity")
a = data[data["proximity"] == "immediate"]
len(a[a["rssi"] == 0])/len(a)

# The first idea is to remove the outliers within the far and immediate categories.
data = data.drop(data[(data["rssi"] == 0) & (data["proximity"] == "immediate")].index)
data = data.drop(data[(data["rssi"] >= 0) & (data["proximity"] == "far")].index)




