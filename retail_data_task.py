# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 23:28:19 2020

@author: Oscar
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import date


data = pd.read_csv("C:/Users/Oscar/Desktop/UOxford/Beacon dataset/beacon_data.csv", sep = ';')

data.head()
# SVM: Using multiple features (location, distance, RSSI, length of stay etc.), 
# predict for a particular application (vendor id) the number of sale in a day 
# is above a contain level.


### 1. Check if the columns have NA values #### 

for column in data:
    print(column +' '+ str(data[column].isnull().values.any()) +' '+str(sum(data[column].isnull())/len(data)))


### 2. Check if the variables entry_date and exit_date are identical when signal_type == 4. In this case I will remove NA values

def countboth(dataset):
    data_noNA_dates = dataset[["signal_type","entry_date","exit_date"]].dropna()
    cases = 0
    for i in range(0,len(data_noNA_dates)):
        if data_noNA_dates["entry_date"].iloc[i] == data_noNA_dates["exit_date"].iloc[i] and data_noNA_dates["signal_type"].iloc[i] ==4:
            cases += 1
        else:
            cases +=0;
    return(cases/len(data_noNA_dates))

countboth(data)

## Remove unuseful columns

data = data.drop("id",axis = 1) # choose variable id or gtid. Both are almost similar.
data = data.drop("merchant_id",axis = 1) # unique ID
data = data.drop("dongle_id",axis = 1) # unique ID
data = data.drop("exit_date",axis = 1) # entry_date = exit_date when signal = 4


### 3. Duplicated values using columns from vendor_id 
# I removed all the repeated values that I found

duplicated_values = data.iloc[:,1:len(data.columns)].duplicated() #there are duplicated values
sum(duplicated_values)/len(duplicated_values) # 4.6% of the rows are duplicated.
data = data[duplicated_values == False] # removed the duplicated rows


#### 4. Analysis of dispersion of the variables (as appropriate):

data.boxplot(column = "rssi",by = "proximity")
data = data[data["rssi"] <= 0] # Remove rows when rssi > 0
data.rssi.value_counts() # replace immediate == 0 by median or mean (optional)
data.loc[(data.rssi == 0) & (data.proximity == "immediate"),"rssi"] = data[(data.proximity == "immediate")].rssi.median() # When proximity == immediate and rssi == 0 then replace those values using the median.

### 5. First idea (not the best by the way): delete those "unknown" records
# New dataset: data_1
# Why not replace these values ​​with "far"? Because I think we would be contaminating some records. I believe that not all of them are 'far'. In the second stage I want to apply it could be to apply KNN to solve this problem using latitude and longitude.

data_1 = data[data["proximity"] != "unknown"]
data_1.iloc[:,5:len(data_1)].describe() # there are records with zero
data_1.boxplot(column = "latitude", by = "proximity")

latitude_immediate=data_1[data_1.proximity == "immediate"].latitude.value_counts()
latitude_near=data_1[data_1.proximity == "near"].latitude.value_counts()
latitude_far=data_1[data_1.proximity == "far"].latitude.value_counts()

longitude_immediate=data_1[data_1.proximity == "immediate"].longitude.value_counts()
longitude_near=data_1[data_1.proximity == "near"].longitude.value_counts()
longitude_far=data_1[data_1.proximity == "far"].longitude.value_counts()


data_1.loc[(data_1.proximity == "immediate") & (data_1.latitude == 0),"latitude"] = latitude_immediate.index[1]
data_1.loc[(data_1.proximity == "near") & (data_1.latitude == 0),"latitude"] = latitude_near.index[0]
data_1.loc[(data_1.proximity == "far") & (data_1.latitude == 0),"latitude"] = latitude_far.index[0]

data_1.loc[(data_1.proximity == "immediate") & (data_1.longitude ==0),"longitude"] = longitude_immediate.index[1]
data_1.loc[(data_1.proximity == "near") & (data_1.longitude ==0),"longitude"] = longitude_near.index[0]
data_1.loc[(data_1.proximity == "far") & (data_1.longitude ==0),"longitude"] = longitude_far.index[0]


### 5.1. Modify dates
data_1 = data_1.sort_values(by = ["subscriber_id","entry_date"], ascending = True)

data_1["entry_date"] = pd.to_datetime(data_1["entry_date"])
data_1["day_entry_date"] = [d.date() for d in data_1["entry_date"]]
data_1["time_entry_date"] = [d.time() for d in data_1["entry_date"]]

def week_of_month(date_value):
 return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)

data_1["month"] = data_1.entry_date.dt.strftime("%B")
data_1["week"] = [week_of_month(d) for d in data_1["entry_date"]]
data_1["day"] = [(d.weekday()+1) for d in data_1["entry_date"]] 
data_1["day"] = ['weekend' if d in [6,7] else 'weekday' for d in data_1["entry_date"]]


### 5. 1 Average time per customer 


time_x = data_1.loc[:,["vendor_id","subscriber_id","day_entry_date","entry_date","month","week","day"]] #select useful columns to calculate this metric

time_x = time_x.groupby(["vendor_id","subscriber_id","day_entry_date","month","week","day"], as_index=False).entry_date.agg(['min','max']).reset_index() #check min and max time

time_x = time_x.rename(columns = {'min':'min_time','max':'max_time'})
time_x["dif_time_minutes"] = (time_x.max_time - time_x.min_time).dt.seconds/60 #calculate the difference in minutes

time_x = time_x.drop(["subscriber_id","day_entry_date","min_time","max_time"], axis = 1) # remove columns

time_x=time_x.groupby(["vendor_id","month","week","day"]).agg({"dif_time_minutes":"mean"}).rename(columns = {"dif_time_minutes":"mean_time_minutes"}).reset_index() #calcualte the mean


### 5.2 Create the target dataframe
# Target_Y (considering "near" and "immediate")

target_y = data_1[data["proximity"].isin(["immediate","near"])].loc[:,["vendor_id","subscriber_id","day_entry_date","entry_date","month","week","day"]]

target_y["month"] = target_y.entry_date.dt.strftime("%B")
target_y["week"] = [week_of_month(d) for d in target_y["day_entry_date"]]
target_y["day"] = [(d.weekday()+1) for d in target_y["day_entry_date"]]
target_y["day"] = ['weekend' if d in [6,7] else 'weekday' for d in target_y["day"]]

target_y = target_y.drop("entry_date", axis = 1)
target_y = target_y.drop("day_entry_date", axis = 1) #Optional

target_y=target_y.groupby(["vendor_id","month","week","day"]).agg({"subscriber_id":pd.Series.nunique}).rename(columns = {"subscriber_id":"subscriber_unique"}).reset_index()


### 5.3 Create a dataframe for the independat variables

variables_x = data_1.drop(["latitude","longitude","signal_type","time_entry_date","proximity","entry_date","day_entry_date"], axis =1)

variables_x = variables_x.groupby(["vendor_id","month","week","day"]).agg({"gtid":"size","subscriber_id":pd.Series.nunique,"distance":"mean","rssi":"mean"}).rename(columns={"gtid":"gtid_count","subscriber_id":"subscriber_id_count","distance":"distance_mean","rssi":"rssi_mean"}).reset_index()

### 5.4 Left Join betwen tables variables_x, time_x and target_y 

# Merge variable_x and time_x 

final_df = pd.merge(variables_x,time_x, how = "left", on =["vendor_id","month","week","day"])

# add the table target_y

final_df= pd.merge(final_df,target_y, how = "left", on =["vendor_id","month","week","day"])
final_df.insert(6,"frequency",final_df.gtid_count/final_df.subscriber_id_count)

final_df["subscriber_unique"] = final_df["subscriber_unique"].fillna(0)


