"""
IconLayer
=========

Location of biergartens in Germany listed on OpenStreetMap as of early 2020.
"""

import pydeck as pdk
import pandas as pd


# Data from OpenStreetMap, accessed via osmpy
#DATA_URL = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/biergartens.json"
#ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png"
# local URL work only with http-server, not with file:

rawData = [{"lat":50.5112014,"lon":6.9939896,"tags":"No listed name"},
           {"lat":49.9534891,"lon":10.8750469,"tags":"No listed name"},
           {"lat":52.4333644,"lon":13.190734,"tags":"Spinnerbr\u00fccke"},
           {"lat":50.0110113,"lon":8.3917604,"tags":"Gasthof Wiesenm\u00fchle"},
           {"lat":48.9693881,"lon":8.3903784,"tags":"No listed name"},
           {"lat":52.4200885,"lon":13.1763456,"tags":"Loretta"},
           {"lat":50.3638373,"lon":7.5769021,"tags":"No listed name"},
           {"lat":52.9822191,"lon":8.845254,"tags":"Schwarzbiergarten"},
           {"lat":49.4814353,"lon":10.993033,"tags":"No listed name"},
           {"lat":47.9927509,"lon":7.8558873,"tags":"Kastaniengarten"},
           {"lat":49.9322248,"lon":11.5720575,"tags":"R\u00f6hrensee"},
           {"lat":48.0124776,"lon":7.8149142,"tags":"Biergarten am Seepark"},
           {"lat":47.9207025,"lon":11.7554223,"tags":"Zum Bartewirt"}
           ]
 
DATA_URL = "georesults.json"


ICON_URL = "/out.png"
GOOD_URL = "/good.png"
BAD_URL = "/pad.png"

icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": GOOD_URL,
    "width": 64,
    "height": 64,
    "anchorY": 64,
}

data = pd.read_json(DATA_URL)
#data = pd.DataFrame(rawData)

def setIcon(x):
    i = icon_data.copy()
    if x != "solved":
        i["url"] = "/bad.png"
    return i
        

data["icon_data"] = None

data.icon_data = data.status.apply(setIcon)

#for i in data.index:
#    data["icon_data"][i] = icon_data

# compute_view(points, view_proportion=1, view_type=<class 'pydeck.bindings.view_state.ViewState'>)
# Automatically computes a zoom level for the points passed in.

# compute view must be adjusted somehow. try without proportion    
view_state = pdk.data_utils.compute_view(data[["lon", "lat"]]) #, 0.1)

icon_layer = pdk.Layer(
    type="IconLayer",
    data=data,
    get_icon="icon_data",
    get_size=20,
    size_scale=1,
    get_position=["lon", "lat"],
    pickable=True,
)

r = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip={"text": "{city}"})
r.to_html("icon_layer.html")
