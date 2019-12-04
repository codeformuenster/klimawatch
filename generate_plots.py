# plots
import plotly.graph_objects as go
# make it easier with numeric values
import pandas
import numpy as np
# for computing the trend
from scipy.stats import linregress
# reading command line arguments
import sys
# writing json
import json

# read data
if(len(sys.argv) == 1):
  print("No city given, plotting data for Münster ('data/muenster.csv')")
  city = "muenster"
  df = pandas.read_csv("data/muenster.csv")
else:
  print("Plotting data for", sys.argv[1])
  city = sys.argv[1]
  try:
    df = pandas.read_csv("data/" + city + ".csv")
  except:
    print("File not found. Does the file data/", city + ".csv",  "exist?")
    exit();

# create plot
fig = go.Figure()

emission_1990 = {}

# compute category-wise percentage (compared to 1990)
for cat in set(df.category):
  if(cat != "Einwohner"):
    emission_1990[str(cat)] = float(df[(df.year == 1990) & (df.category == cat) & (df.type == "real")].value)

    df.loc[df.category == cat, 'percentage'] = df[df.category == cat].value / emission_1990[str(cat)]

# set() only lists unique values
# this loop plots all categories present in the csv, if type is either "real" or "geplant"
for cat in set(df.category):
  subdf = df[(df.category == cat) & (df.type != "Einwohner")]

  subdf_real = subdf[subdf.type == "real"]

  fig.add_trace(go.Scatter(x = subdf_real.year, y = subdf_real.value,
                          name = cat + ", real", mode = "lines+markers",
                          legendgroup = cat,
                          text = subdf_real.percentage,
                          hovertemplate =
                            "<b>tatsächliche</b> Emissionen, Kategorie: " + cat +
                            "<br>Jahr: %{x}<br>" +
                            "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>" +
                            "Prozent von Emissionen 1990: " + "%{text:.0%}" +
                            "<extra></extra>") # no additional legend text in tooltip
                )

  subdf_planned = subdf[subdf.type == "geplant"]
  fig.add_trace(go.Scatter(x = subdf_planned.year, y = subdf_planned.value, name = cat + ", geplant",
                          mode = "lines+markers", line = dict(dash = "dash"),
                          legendgroup = cat,
                          text = subdf_planned.percentage,
                           hovertemplate =
                            "<b>geplante</b> Emissionen, Kategorie: " + cat +
                            "<br>Jahr: %{x}<br>" +
                            "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>" +
                            "Prozent von Emissionen 1990: " + "%{text:.0%}" +
                            "<extra></extra>") # no additional legend text in tooltip
                )

# compute trend based on current data
subdf = df[df.category == "Gesamt"]
subdf_real = subdf[subdf.type == "real"]

# variables to write to JSON later on
years_past_total_real = list(subdf_real.year)
values_past_total_real = list(subdf_real.value)

slope, intercept, r, p, stderr = linregress(subdf_real.year, subdf_real.value)
# print info about trend
print("linearer Trend: Steigung: ", slope, "Y-Achsenabschnitt: ",  intercept, "R^2: ", r)

# plot trend
fig.add_trace(go.Scatter(x = subdf.year, y = slope * subdf.year + intercept, name = "Trend",
                          mode = "lines", line = dict(dash = "dot"),
                          legendgroup = "future",
                          text = (slope * subdf.year + intercept) / emission_1990["Gesamt"],
                          hovertemplate =
                            "<b>bisheriger Trend</b>" +
                            "<br>Jahr: %{x}<br>" +
                            "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>" +
                            "Prozent von Emissionen 1990: " + "%{text:.0%}" +
                            "<extra></extra>") # no additional legend text in tooltip
             )


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

# TODO: make df instead of (double) calculation inline?
fig.add_trace(go.Scatter(x = np.array(future) + 2020, y = paris_slope * np.array(future) + last_emissions,
                          name = "Paris berechnet",
                          mode = "lines+markers", line = dict(dash = "dash"),
                          legendgroup = "future",
                          text = (paris_slope * np.array(future) + last_emissions) / emission_1990["Gesamt"],
                          hovertemplate =
                            "<b>Paris-Budget</b>" +
                            "<br>Jahr: %{x:.0f}<br>" +
                            "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>" +
                            "Prozent von Gesamt-Emissionen 1990: " + "%{text:.0%}" +
                            "<extra></extra>") # no additional legend text in tooltip
             )

fig.add_trace(go.Scatter(
  x = [2020],
  y = [emission_1990["Gesamt"] + (emission_1990["Gesamt"] / 30)],
  mode = "text",
  text = "heute",
  hoverinfo="none",
  showlegend = False)
)

# horizontal legend; vertical line at 2020
fig.update_layout(
  title = "Realität und Ziele",
  yaxis_title = "CO<sub>2</sub> in tausend Tonnen",
  xaxis_title = "Jahr",
  # horizontal legend
  legend_orientation = "h",
  # put legend above plot to avoid overlapping-bug
  legend_xanchor = "center",
  legend_y = -0.25,
  legend_x = 0.5,
  legend_font_size = 10,
  # disable dragmode for better mobile experience
  dragmode = False,
  # German number separators
  separators = ",.",
  # vertical "today" line
  shapes = [
    go.layout.Shape(
      type = "line",
      x0 = 2020,
      y0 = 0,
      x1 = 2020,
      y1 = emission_1990["Gesamt"],
    )]
  )

# write plot to file
fig.write_html("hugo/layouts/shortcodes/paris_" + city + ".html", include_plotlyjs = False,
                config = {'displayModeBar': False}, full_html = False, auto_open = True)

# write computed Paris budget to JSON file for you-draw-it

paris_data = {}
paris_data["values"] = []

# past data

for index in range(len(years_past_total_real)):
  paris_data["values"].append({
      "year": years_past_total_real[index],
      "value": values_past_total_real[index]
  })

# years with remaining budget
paris_years = list(np.array(future) + 2020)
budget_per_year = list(paris_slope * np.array(future) + last_emissions)

for index in range(len(paris_years)):
  paris_data["values"].append({
      "year": paris_years[index],
      "value": budget_per_year[index]
  })

# fill up zeros to let people draw until 2050
# ~ years_until_2050 =

climate_neutral_by = int(np.round(max(paris_years)))
years_after_budget = range(climate_neutral_by, 2051, 1)

for y in years_after_budget:
  paris_data["values"].append({
      "year": y,
      "value": 0
  })

with open("hugo/data/you_draw_it_" + city + "_paris_data.json", "w") as outfile:
    json.dump(paris_data, outfile, indent = 2)

# TODO visualise modules

fig_modules = go.Figure(go.Treemap(
    branchvalues = "total",
    labels = ["Wärme", "Strom", "Verkehr",  "W1", "W2", "S1", "S2", "V1", "V2"],
    parents = ["", "", "", "Wärme", "Wärme", "Strom", "Strom", "Verkehr", "Verkehr"],
    values = [780, 690, 484, 700, 80, 600, 90, 400, 84],
    marker_colors = ["green", "yellow", "red", "green", "green", "red", "green", "red", "red"],
    textinfo = "label+value+percent parent+percent entry+percent root",
))

fig_modules.write_html("hugo/layouts/shortcodes/modules_" + city + ".html", include_plotlyjs = False,
                        config={'displayModeBar': False}, full_html = False, auto_open=True)

