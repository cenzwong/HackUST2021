#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import requests
import json
import datetime
import time

response = requests.get("https://raw.githubusercontent.com/mwgg/Airports/master/airports.json")
raw_transport_code = json.loads(response.text)
pd_raw_transport_code = pd.DataFrame(raw_transport_code)
pd_airport_ICAO_code = pd_raw_transport_code
pd_airport_ICAO_code = pd_airport_ICAO_code.T

from math import sin, cos, sqrt, atan2, radians

all_airport_lat = pd_airport_ICAO_code['lat']
all_airport_lon = pd_airport_ICAO_code['lon']

all_airport_lat = list(all_airport_lat)
all_airport_lon = list(all_airport_lon)
possible_airport_lat = 0
possible_airport_lon = 0
list_possible_airport_lon = []
list_possible_airport_lat = []
possible_airport_lat = float(possible_airport_lat)
possible_airport_lon = float(possible_airport_lon)

for i in range(len(all_airport_lat)):
    all_airport_lat[i] = float(all_airport_lat[i])
    all_airport_lon[i] = float(all_airport_lon[i])
    
pd_airport_ICAO_code = pd_airport_ICAO_code.assign(float_lat = all_airport_lat)
pd_airport_ICAO_code = pd_airport_ICAO_code.assign(float_lon = all_airport_lon)
distance_from_airport = []

for i in range(len(all_airport_lat)):
    # approximate radius of earth in km
    R = 6373.0

    lat_gps = radians(51.465003)
    lon_gps = radians(-0.470441)
    lat_airport_i = radians(all_airport_lat[i])
    lon_airport_i = radians(all_airport_lon[i])

    distance_lon = lon_airport_i - lon_gps
    distance_lat = lat_airport_i - lat_gps

    a = sin(distance_lat / 2)**2 + cos(lat_gps) * cos(lat_airport_i) * sin(distance_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    
    if distance <= 10:
        distance_from_airport.append(distance)
        list_possible_airport_lat.append(all_airport_lat[i])
        list_possible_airport_lon.append(all_airport_lon[i])

        
    else:
        continue
        
        
for i in range(len(distance_from_airport)):
    if len(distance_from_airport)==1:
        possible_airport_lat = list_possible_airport_lat[i]
        possible_airport_lon = list_possible_airport_lon[i]
    else:
        for j in range(len(distance_from_airport)):
            if distance_from_airport[i] < distance_from_airport[j]:
                possible_airport_lat = list_possible_airport_lat[i]
                possible_airport_lon = list_possible_airport_lon[i]

            else:
                continue
        
print(possible_airport_lat,possible_airport_lon)
departure_airport = pd_airport_ICAO_code[(pd_airport_ICAO_code['float_lat'] == possible_airport_lat) & (pd_airport_ICAO_code['float_lon'] == possible_airport_lon)]
print(departure_airport)
print(distance_from_airport)


# In[ ]:




