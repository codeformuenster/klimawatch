
from geopy.geocoders import Nominatim
import pandas as pd
import json
import os
import sys
import time


geolocator = Nominatim(user_agent="digital-codes")

useNominatim = True

base = os.sep.join(["data/fragdenstaat"])
df = pd.read_json(os.sep.join([base,"messages.json"]))
g = df.groupby(by="request_id")
failed = []
solved = []
for i,gg in g:
    if gg[gg.status == "resolved"].empty:
        #print("No data for ",i)
        failed.append(i)
    else:
        #print(i," OK")
        solved.append(i)

print(f"Failed: {len(failed)}, solved: {len(solved)}")

# https://stackoverflow.com/questions/1981349/regex-to-replace-multiple-spaces-with-a-single-space

def readItem(s):
    with open(os.sep.join([base,f"{s}.json"])) as f:
        r = json.load(f)
        # replace all whitespace with single blank
        addr = " ".join(r["public_body"]["address"].split()).split(" ")
        #print(addr)
        # try to find PLZ in addr
        addrOk = False
        for i,p in enumerate(addr):
            # there are wrong plz entries like 2072236 Freudenstadt
            # check for numic first
            if p.isnumeric():
                if len(p) >= 5:
                    addrOk = True
                    plz = p[len(p)-5:]
                    city = addr[i+1]
                    # chcek for leading bad
                    if (city.lower() == "bad") and (len(addr) > i+1):
                        city = " ".join([addr[i+1],addr[i+2]]).strip()
                    result =  {
                                "id":s,
                                "plz":plz,
                                "city":city
                            }
                    if useNominatim:
                        try:
                            print(s)
                            loc = geolocator.geocode({"postcode":result["plz"],"city":result["city"],"country":"Germany"})
                            result["lat"] = loc.latitude
                            result["lon"] = loc.longitude
                            result["geoaddr"] = loc.address
                            if not result["city"].lower() in result["geoaddr"].lower():
                                print("Suspicous:",result)
                            time.sleep(1.1)
                        except:
                            print("Failed on ",result)
                            return None

                    #print(f"{i},{p} {addr[i+1]}")
                    # expect city to be in geocoded result
                    return result
                
        if not addrOk:
            print("Invalid:",s,"-",r["public_body"]["address"])
            return None

    

# go to the requests
base = os.sep.join(["data/fragdenstaat/requests"])
df = pd.DataFrame()
for s in solved:
    r = readItem(s)
    if r != None:
        r["status"] = "solved"
        if df.empty:
            df = pd.DataFrame(r,index=[0])
        else:
            df = df.append(r,ignore_index=True)

for s in failed:
    r = readItem(s)
    if r != None:
        r["status"] = "failed"
        if df.empty:
            df = pd.DataFrame(r,index=[0])
        else:
            df = df.append(r,ignore_index=True)


df.to_json("georesults.json",orient="records")
