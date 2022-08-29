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

datadir = "/home/kugel/devel/okl/klimawatch/data"

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
    # force lower case
    locs.name = locs.apply(lambda x: x["name"].lower(), axis=1)
    print("Locs available")
    readLocs = False
except:
    geolocator = Nominatim(user_agent="klimawatch")
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
            if c.lower() in locs.name.values:
                loc = locs[locs.name == c]
            else:
                # reading
                print("Reading ",c)
                loc = geolocator.geocode({"city":c,"country":"Germany"})
                locs=locs.append({"name":c,"address":loc.address,"latitude":loc.latitude,"longitude":loc.longitude},ignore_index=True)
                loc = locs[locs.name == c] # reread to get same format
                readLocs = True # need to write back
                
##            if readLocs:
##                loc = geolocator.geocode({"city":c,"country":"Germany"})
##                locs=locs.append({"name":c,"address":loc.address,"latitude":loc.latitude,"longitude":loc.longitude},ignore_index=True)
##                loc = locs[locs.name == c] # reread to get same format
##            else:
##                loc = locs[locs.name == c]

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
                # VALUE: to t from kilo-t
                realItems = {
                        "name":city,
                        "value":round(last.co2.values[0]/pop.co2.values[0]*10000)/10,
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
                        "value":round(getPco2(plan,last)/pop.co2.values[0]*10000)/10,
                        "type":"Plan",
                        "lng": lon - .05,
                        "lat": lat - .05,
                        "pop":pop.co2.values[0],
                        "year":getPyear(plan,last),
                        "co2":getPco2(plan,last),
                        "color":planColor
                        }
                # without progress data we copy real times 
                progressItems = {
                        "name":city,
                        "value":round(last.co2.values[0]/pop.co2.values[0]*10000)/10,
                        "type":"Fortschritt",
                        "lng": lon - .05,
                        "lat": lat + .05,
                        "pop":pop.co2.values[0],
                        "year":last.year.values[0],
                        "co2":last.co2.values[0],
                        "color":[0,200,200]
                        }
                #print("Items:",items)
                cityData = cityData.append(realItems,ignore_index=True)
                cityData = cityData.append(planItems,ignore_index=True)
                cityData = cityData.append(progressItems,ignore_index=True)
            except:
                print("failed:", f,"\nlast ",last,"\npop ",pop,"\nplan ",plan)
                continue

if readLocs:
    locs.to_csv("locs.csv",index=False)



# ##################
ICON_FILE = "georesults.json"

ATTACH_FILE = "../data/fragdenstaat/attachments.json"
att = pd.read_json(ATTACH_FILE)

icon_urls = {
    "error":"/error.png",
    "pdf":"/pdf.png",
    "delay":"/delay.png",
    "table":"/table.png"
    }

icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": icon_urls["error"],
    "width": 64,
    "height": 64,
    "anchorY": 64,
}

# read icon locations
icons = pd.read_json(ICON_FILE)

#    att[att.id == 231612].name.values[0].lower().endswith(".pdf")

def setIcon(status,id):
    i = icon_data.copy()
    if status != "solved":
        i["url"] = icon_urls["delay"]
    else:
        i["url"] = icon_urls["error"]
        if not att[att.request_id == id].empty:
            print("Check",id)
            if att[att.request_id == id].name.values[0].lower().endswith(".pdf"):
                i["url"] = icon_urls["pdf"]
            elif att[att.request_id == id].name.values[0].lower().find(".xls")>=0:
                i["url"] = icon_urls["table"]
    return i   

    
# df['col_3'] = df.apply(lambda x: f(x.col_1, x.col_2), axis=1)

icons["icon_data"] = None

icons.icon_data = icons.apply(lambda x: setIcon(x["status"],x["id"]), axis=1)

# copy icon url to base object
icons["icon"] = icons.icon_data.apply(lambda x :x["url"])

print("Groups: ",icons.groupby(by="icon").size())

def getValue(x):
    for k in icon_urls:
        if x == icon_urls[k]:
            return k

    

# copy some other values for pydeck tooltip
icons["name"] = icons.city
icons["value"] = icons.icon.apply(getValue)
icons["type"] = "Frag den Staat"


icon_layer = pdk.Layer(
    type="IconLayer",
    data=icons,
    get_icon="icon_data",
    get_size=20,
    size_scale=1,
    get_position=["lon", "lat"],
    pickable=True,
    
)


# ###################


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
    elevationScale = 10000,

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
r = pdk.Deck(layers=[icon_layer,layer],
             initial_view_state=view_state,map_style="light",
             tooltip=tooltip
    )


r.to_html("klimawatch.html")

