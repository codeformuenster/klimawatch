
from geopy.geocoders import Nominatim
import pandas as pd
import json
import os
import sys
import time


# try to read existing geo file first
try:
    geofile = pd.read_json("georesults.json")
except:
    print("No geofile")
    geofile = pd.DataFrame()

geolocator = Nominatim(user_agent="digital-codes")

useNominatim = True

# https://stackoverflow.com/questions/1981349/regex-to-replace-multiple-spaces-with-a-single-space

def readItem(s):
    with open(os.sep.join([base,f"{s}.json"])) as f:
        r = json.load(f)
        # replace all whitespace with single blank
        addr = " ".join(r["public_body"]["address"].split()).split(" ")
        #print(addr)
        # try to find PLZ in addr
        addrOk = False
        if not "geo" in r["public_body"].keys() or r["public_body"]["geo"] == None:
            print("Missing geo: ",s)

            #check geofile first
            if not geofile[geofile.id == int(s)].empty:
                item = geofile[geofile.id == int(s)]
                coords = {"coordinates":[item.lat.values[0],item.lon.values[0]]}
                # insert coordinates
                r["public_body"]["geo"] = coords
                useNominatim = False
            else:
                useNominatim = True
        else:
            # print("geo", r["public_body"]["geo"])
            useNominatim = False
            
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
                                #"url": f'https://fragdenstaat.de/{r["url"]}',
                                "url": "".join(["https://fragdenstaat.de",r["url"]]),
                                "plz":plz,
                                "city":city
                            }
                    if useNominatim:
                        print("Nominatim required on: ",s)
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
                    else:
                        # use geo field
                        if "geo" in r["public_body"].keys() and r["public_body"]["geo"] != None:
                            geo = list(r["public_body"]["geo"]["coordinates"])
                            result["lat"] = geo[1]
                            result["lon"] = geo[0]
                            result["geoaddr"] = " ".join([plz,city,"Deutschland"])

                    #print(f"{i},{p} {addr[i+1]}")
                    # expect city to be in geocoded result
                    # insert status from resultion field:
##                    SUCCESSFUL = "successful", _("Request Successful")
##                    PARTIALLY_SUCCESSFUL = "partially_successful", _("Request partially successful")
##                    NOT_HELD = "not_held", _("Information not held")
##                    REFUSED = "refused", _("Request refused")
##                    USER_WITHDREW_COSTS = "user_withdrew_costs", _("Request was withdrawn due to costs")
##                    USER_WITHDREW = "user_withdrew", _("Request was withdrawn")

                    if "successful" in r["resolution"]:
                        result["status"] = "solved"
                    else:
                        result["status"] = "failed"
                    return result
                
        if not addrOk:
            print("Invalid:",s,"-",r["public_body"]["address"])
            return None

    

# go to the requests
base = os.sep.join(["data/fragdenstaat/requests"])
requests = [x.split(".json")[0] for x in os.listdir(base)]

df = pd.DataFrame()
for s in requests:
    r = readItem(s)
    if r != None:
        if df.empty:
            df = pd.DataFrame(r,index=[0])
        else:
            df = df.append(r,ignore_index=True)



df.to_json("georesults.json",orient="records")
