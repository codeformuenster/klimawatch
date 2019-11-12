# plots
import plotly.graph_objects as go
# make it easier with numeric values
import pandas
import numpy as np
# for computing the trend
from scipy.stats import linregress
# reading command line arguments
import sys

# read data
if(len(sys.argv) == 1):
  print("No city given, plotting data for Münster ('muenster.csv')")
  df = pandas.read_csv("muenster.csv")
else:
  print("Plotting data for", sys.argv[1])
  df = pandas.read_csv(sys.argv[1] + ".csv")

# create plot
fig = go.Figure()

# set() only lists unique values
# this loop plots all categories present in the csv, if type is either "real" or "geplant"
for cat in set(df.category):
  subdf = df[df.category == cat]
  subdf_real = subdf[subdf.type == "real"]
  fig.add_trace(go.Scatter(x = subdf_real.year, y = subdf_real.value, name = cat + ", real",
                          mode = "lines+markers"))

  subdf_planned = subdf[subdf.type == "geplant"]
  fig.add_trace(go.Scatter(x = subdf_planned.year, y = subdf_planned.value, name = cat + ", geplant",
                          mode = "lines+markers", line = dict(dash = "dash")))

# compute trend based on current data
subdf = df[df.category == "Gesamt"]
subdf_real = subdf[subdf.type == "real"]

slope, intercept, r, p, stderr = linregress(subdf_real.year, subdf_real.value)
# print info about trend
print("linearer Trend: Steigung: ", slope, "Y-Achsenabschnitt: ",  intercept, "R^2: ", r)

# plot trend
fig.add_trace(go.Scatter(x = subdf.year, y = slope * subdf.year + intercept, name = "Trend",
                          mode = "lines", line = dict(dash = "dot")))


# compute remaining paris budget
last_emissions = np.array(df[df.note == "last_emissions"].value)
# see https://scilogs.spektrum.de/klimalounge/wie-viel-co2-kann-deutschland-noch-ausstossen/
paris_budget_germany_2019 = 7300000
inhabitants_germany = 83019213
paris_budget_per_capita_2019 = paris_budget_germany_2019 / inhabitants_germany
paris_budget_full_city_2019 = paris_budget_per_capita_2019 * np.array(df[df.type == "Einwohner"].value)
# substract individual CO2 use; roughly 40%, see https://uba.co2-rechner.de/
paris_budget_wo_individual_city_2019 = paris_budget_full_city_2019 * 0.6
# substract already emitted CO2 from 2019 onwards; assume last measured budget is 2019 emission
paris_budget_wo_individual_city_2020 = paris_budget_wo_individual_city_2019 - last_emissions

# compute slope for linear reduction of paris budget
paris_slope = (-pow(last_emissions, 2)) / (2 * paris_budget_wo_individual_city_2020)
years_to_climate_neutral = - last_emissions / paris_slope
full_years_to_climate_neutral = int(np.round(years_to_climate_neutral))

# plot paris line
future = list(range(0, full_years_to_climate_neutral, 1)) # from 2020 to 2050
future.append(float(years_to_climate_neutral))
fig.add_trace(go.Scatter(x = np.array(future) + 2020, y = paris_slope * np.array(future) + last_emissions, name = "Paris berechnet",
                          mode = "lines+markers", line = dict(dash = "dash")))

# horizontal legend; vertical line at 2020
fig.update_layout(
  legend_orientation="h",
  # vertical "today" line
  shapes=[
    go.layout.Shape(
      type="line",
      x0=2020,
      y0=0,
      x1=2020,
      y1=2500,
    )]
  )

# write plot to file
fig.write_html('plotly_paris.html', include_plotlyjs = "cdn", full_html = False, auto_open=True)

# TODO add percentage to plotly tooltips
# ~ percentage_real = [x / data_real.data["CO2"][0] for x in data_real.data["CO2"]]
# ~ data_real.add(name = "percentage", data = percentage_real)

# ~ percentage_warmth_real = [x / data_warmth_real.data["CO2"][0] for x in data_warmth_real.data["CO2"]]
# ~ data_warmth_real.add(name = "percentage", data = percentage_warmth_real)

# ~ percentage_electricity_real = [x / data_electricity_real.data["CO2"][0] for x in data_electricity_real.data["CO2"]]
# ~ data_electricity_real.add(name = "percentage", data = percentage_electricity_real)

# ~ percentage_traffic_real = [x / data_traffic_real.data["CO2"][0] for x in data_traffic_real.data["CO2"]]
# ~ data_traffic_real.add(name = "percentage", data = percentage_traffic_real)

# ~ percentage_planned = [x / data_real.data["CO2"][0] for x in data_planned.data["CO2"]]
# ~ data_planned.add(name = "percentage", data = percentage_planned)

# ~ percentage_trend = [x / data_real.data["CO2"][0] for x in data_trend.data["CO2"]]
# ~ data_trend.add(name = "percentage", data = percentage_trend)

# ~ percentage_paris = [x / data_real.data["CO2"][0] for x in data_paris.data["CO2"]]
# ~ data_paris.add(name = "percentage", data = percentage_paris)

# ~ TOOLTIPS = [
    # ~ ("Jahr", "@year"),
    # ~ ("CO2 (tausend Tonnen)", "@CO2{0.00}"),
    # ~ ("Prozent von 1990", "@percentage{0.0%}"),
    # ~ ("Typ", "@type"),
# ~ ]


# TODO visualise modules

fig_modules = go.Figure(go.Treemap(
    branchvalues = "total",
    labels = ["Wärme", "Strom", "Verkehr",  "W1", "W2", "S1", "S2", "V1", "V2"],
    parents = ["", "", "", "Wärme", "Wärme", "Strom", "Strom", "Verkehr", "Verkehr"],
    values = [780, 690, 484, 700, 80, 600, 90, 400, 84],
    marker_colors = ["green", "yellow", "red", "green", "green", "red", "green", "red", "red"],
    textinfo = "label+value+percent parent+percent entry+percent root",
))

fig_modules.write_html('plotly_modules.html', include_plotlyjs = "cdn", full_html = False, auto_open=True)

