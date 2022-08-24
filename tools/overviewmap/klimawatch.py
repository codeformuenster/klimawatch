#!/usr/bin/env python

import pydeck as pdk
import pandas as pd
import os
import sys
import random
from geopy.geocoders import Nominatim
import time

# animation requires jupyter extension:
# install: (if required)
#[kugel@tux2 python]$ jupyter nbextension install  --overwrite --py pydeck --userInstalling /home/kugel/.local/lib/python3.10/site-packages/pydeck/nbextension/static -> pydeck
# enable: 
# [kugel@tux2 python]$ jupyter nbextension enable pydeck --user --py



# cities
# all files in data dir, extension .csv. Names can be like <city>_something.csv
cities = [
    "berlin",
    "bielefeld",
    "bonn",
    "chemnitz",
    "dortmund",
    "duesseldorf",
    "hamburg",
    "karlsruhe",
    "koeln",
    "landau",
    "leipzig",
    "moers",
    "muenchen",
    "muenster",
    "paderborn",
    "ulm"
]

# csv format: year,category,type,co2,note
# status: look for 2 rows:
# 2017,Gesamt,real,19778,

# 2018,Einwohner,Einwohner,3644826,
# plan: look for
# 2020,Gesamt,geplant,17702,

datadir = "/home/kugel/temp/okl/klimawatch/data"

files = os.listdir(datadir)

def getPyear(plan,last):
    if plan.empty:
        return last.year.values[0]
    else:
        return plan[plan.year == plan.year.max()].year.values[0]

def getPco2(plan,last):
    if plan.empty:
        return last.co2.values[0]
    else:
        return plan[plan.year == plan.year.max()].co2.values[0] + 1 # add one 

cityData = pd.DataFrame(columns=["name","pop","type","value","year","co2","lat","lng","color"])

try: 
    locs = pd.read_csv("locs.csv")
    print("Locs available")
    readLocs = False
except:
    geolocator = Nominatim(user_agent="digital-codes")
    locs = pd.DataFrame(columns=["name","address","latitude","longitude"])
    readLocs = True


for f in files:
    if not ".csv" in f:
        continue
    if "sachstand" in f.lower():
        continue
    for c in cities:
        if f.startswith(c):
            #print(f)
            if readLocs:
                loc = geolocator.geocode({"city":c,"country":"Germany"})
                locs=locs.append({"name":c,"address":loc.address,"latitude":loc.latitude,"longitude":loc.longitude},ignore_index=True)
                loc = locs[locs.name == c] # reread to get same format
            else:
                loc = locs[locs.name == c]
            city = loc.address.values[0].split(",")[0]
            lat = loc.latitude.values[0]
            lon = loc.longitude.values[0]
            #print(name,lat,lon)
            df = pd.read_csv("/".join([datadir,f]))
            #print(df.describe)
            try:
                last = df[df.note == "last_emissions"]
                pop = df[df.category == "Einwohner"]
                plan = df[(df.type == "geplant") & (df.category == "Gesamt")]
                if plan.empty:
                    print(f"{f}: Kein Plan")
                    planColor = [100,0,200]
                else:
                    planColor = [0,200,0]
                #print(last,pop)
                #print("Last:",last.year,last.co2)
                #print("Pop:",pop.year,pop.co2)
                #print("Plan:",plan.year,plan.co2)
                realItems = {
                        "name":city,
                        "value":round(last.co2.values[0]/pop.co2.values[0]*1000)/1000,
                        "type":"Basis",
                        "lng": lon,
                        "lat": lat,
                        "pop":pop.co2.values[0],
                        "year":last.year.values[0],
                        "co2":last.co2.values[0],
                        "color":[200,0,0]
                    }
                planItems = {
                        "name":city,
                        "value":round(getPco2(plan,last)/pop.co2.values[0]*1000)/1000,
                        "type":"Plan",
                        "lng": lon - .03,
                        "lat": lat - .03,
                        "pop":pop.co2.values[0],
                        "year":getPyear(plan,last),
                        "co2":getPco2(plan,last),
                        "color":planColor
                        }
                #print("Items:",items)
                cityData = cityData.append(realItems,ignore_index=True)
                cityData = cityData.append(planItems,ignore_index=True)
            except:
                print("failed:", f,"\nlast ",last,"\npop ",pop,"\nplan ",plan)
                continue

if readLocs:
    locs.to_csv("locs.csv",index=False)


# types:
# map_style (str or dict, default 'dark') – 
#   One of ‘light’, ‘dark’, ‘road’, ‘satellite’, ‘dark_no_labels’, and ‘light_no_labels’,

# provider:
# map_provider (str, default 'carto') – 
#   If multiple API keys are set (e.g., both Mapbox and Google Maps), 
#   inform pydeck which basemap provider to prefer. Values can be carto, mapbox or google_maps

MB_KEY = ""

keys = {"mapbox":MB_KEY}

# Define a layer to display on a map
layer = pdk.Layer(
    "ColumnLayer",
    cityData,

    diskResolution = 12,
    radius = 2500,
    extruded = True,
    pickable =  True,
    elevationScale = 10000000,

    getFillColor = "color",
    getLineColor = [0, 0, 200],
    getElevation = "value",
    
    get_position = ["lng", "lat"]
)


# Set the viewport location
view_state = pdk.ViewState(
    longitude=10.0, latitude=50, zoom=5, min_zoom=5, max_zoom=15, pitch=50, bearing=0
    #longitude=8.4, latitude=49, zoom=8, min_zoom=5, max_zoom=15, pitch=40.5, bearing=-27.36,
)

tooltip = {
    "text": "{name} - {type}: {value}"
}

# Render
#r = pdk.Deck(layers=[layer], initial_view_state=view_state,map_style="dark",map_provider="mapbox",api_keys=keys)
r = pdk.Deck(layers=[layer],
             initial_view_state=view_state,map_style="dark",
             tooltip=tooltip
    )


r.to_html("klimawatch.html")

