#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import requests
import json
import datetime
import time

response = requests.get("https://www.lux-airport.lu/wp-content/themes/lux-airport/flightsinfo.php?arrivalsDepartures_action=getArrivalsDepartures&lang=en")


# load json object to python object
airport_dict = json.loads(response.text)


# load dictionary to DataFrames
airport_df = pd.DataFrame(airport_dict['departures'])


possible = airport_df[airport_df['remarks']=='Take Off']

raw_date = possible['scheduledDate']
raw_time = possible['scheduledTime']



#change date time to unix timestamp
list_date = list(raw_date)
list_time = list(raw_time)
seperated_date_and_time = []
for i in range(len(list_date)):
    seperated_date_and_time.append([])
    seperated_date_and_time[i].append(list_date[i].split("-"))
    seperated_date_and_time[i].append(list_time[i].split(":"))
    seperated_date_and_time[i] =  seperated_date_and_time[i][0] + seperated_date_and_time[i][1]
    for j in range(len(seperated_date_and_time[i])):
        int_date_time = int(seperated_date_and_time[i][0])
        seperated_date_and_time[i].remove(seperated_date_and_time[i][0])
        seperated_date_and_time[i].append(int_date_time)
        
    seperated_date_and_time[i][3] -= 2



import datetime
import time
from datetime import timezone

unixtime =[]

for i in range(len(seperated_date_and_time)):
    date_time_string = '-'.join([str(elem) for elem in seperated_date_and_time[i]])
    element = datetime.datetime.strptime(date_time_string,"%Y-%m-%d-%H-%M")
    timestamp = element.replace(tzinfo=timezone.utc).timestamp()
    unixtime.append(timestamp)
    

possible_with_unix_Timestamp = possible.assign(UnixTimestamp = unixtime)


time_now = time.time()
int(time_now)
Nve_now = time_now - 3600*3
Pve_now = time_now 
possible_flight = possible_with_unix_Timestamp[(possible_with_unix_Timestamp['UnixTimestamp'] >= Nve_now) & (possible_with_unix_Timestamp['UnixTimestamp'] <= Pve_now)]



possible_flightNumber = possible_flight['flightNumber']
list_possible_flightNumber = list(possible_flightNumber)

list_possible_flightNumber



