#!/usr/bin/env python
# coding: utf-8

# In[84]:


import pandas as pd
import requests
import json
import datetime
import time


# In[85]:


response = requests.get("https://www.lux-airport.lu/wp-content/themes/lux-airport/flightsinfo.php?arrivalsDepartures_action=getArrivalsDepartures&lang=en")


# In[86]:


# load json object to python object
airport_dict = json.loads(response.text)


# In[87]:


airport_dict


# In[88]:


# load dictionary to DataFrames
airport_df = pd.DataFrame(airport_dict['departures'])


# In[89]:


airport_df


# In[90]:


possible = airport_df[airport_df['remarks']=='Take Off']


# In[91]:


possible


# In[92]:


raw_date = possible['scheduledDate']
raw_time = possible['scheduledTime']


# In[ ]:





# In[93]:


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


# In[94]:


import datetime
import time
from datetime import timezone

unixtime =[]

for i in range(len(seperated_date_and_time)):
    date_time_string = '-'.join([str(elem) for elem in seperated_date_and_time[i]])
    element = datetime.datetime.strptime(date_time_string,"%Y-%m-%d-%H-%M")
    timestamp = element.replace(tzinfo=timezone.utc).timestamp()
    unixtime.append(timestamp)
    
print(unixtime)


# In[95]:


possible_with_unix_Timestamp = possible.assign(UnixTimestamp = unixtime)


# In[96]:


possible_with_unix_Timestamp


# In[97]:


possible_flight = possible_with_unix_Timestamp[(possible_with_unix_Timestamp['UnixTimestamp'] >= 1617357600.0) & (possible_with_unix_Timestamp['UnixTimestamp'] <= 1617359100.0)]


# In[98]:


possible_flight


# In[ ]:





# In[ ]:




