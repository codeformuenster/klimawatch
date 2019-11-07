import math
import fileinput

import numpy as np
from sklearn.linear_model import LinearRegression

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components

#######################################
# TODO: read csv and use as data source
# ~ import csv

# ~ with open('data_1990-2050.csv') as csvfile:
  # ~ readCSV = csv.reader(csvfile, delimiter=',')
  # ~ next(readCSV) # skip first row
  # ~ year = []
  # ~ data_complete_real = []
  # ~ for row in readCSV:
    # ~ # TODO: use column names
    # ~ y = row[0]
    # ~ real = row[4]

    # ~ year.append(y)
    # ~ data_complete_real.append(real)

  # ~ print(year)
  # ~ print(data_complete_real)
########################################


year = [1990, 1995, 2000, 2005, 2006, 2010, 2011, 2015, 2016, 2017]
year_future = [2018, 2019, 2020,
                2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,
                2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039,
                2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050]

data_real = ColumnDataSource(data = {
  "year": year,
  "CO2": [2517, 2459, 2471, 2386, 2295, 2116, 2061, 2017, 1981, 1954],
  "type": ["real, gesamt"] * 10
  })

# TODO: data for 2006 is estimated (mean for 2005 and 2010)
# TODO: data for 2015, 2016, 2017 for warmth and electricity is estimated from plots

data_warmth_real = ColumnDataSource(data = {
  "year": year,
  "CO2": [1119, 1060, 1064, 958, 873, 788, 742, 775,780 ,780],
  "type": ["Wärme, real"] * 10
  })

data_electricity_real = ColumnDataSource(data = {
  "year": year,
  "CO2": [819, 822, 839 ,885, 842.5, 800, 789, 750, 710, 690],
  "type": ["Strom, real"] * 10
  })

data_traffic_real = ColumnDataSource(data = {
  "year": year,
  "CO2": [579, 577, 568, 543, 535.5, 528, 530, 492, 491, 484],
  "type": ["Verkehr, real"] * 10
  })

year_complete = year + year_future

data_planned = ColumnDataSource(data = {
  "year": year_complete,
  "CO2": [2517, 2349.2, 2181.4, 2013.6, 1980.04, 1845.8, 1812.24, 1678, 1644.44, 1610.88, 1577.32, 1543.76, 1510.2,
          1464.055, 1417.91, 1371.765, 1325.62, 1279.475, 1233.33, 1187.185, 1141.04, 1094.895,
          1048.75, 1002.605, 956.46, 910.315, 864.17, 818.025, 771.88, 725.735, 679.59, 633.445,
          587.3, 541.155, 495.01, 448.865, 402.72, 356.575, 310.43, 264.285, 218.14, 171.995,
          125.85],
  "type": ["Münsteraner Ziele, gesamt"] * 43
  })

# compute trend based on current data
year_r = np.array(year[0:10]).reshape(-1, 1)
data_r = data_real.data["CO2"][0:10]
model = LinearRegression().fit(year_r, data_r)

r_sq = model.score(year_r, data_r)
print("R^2 linearer Trend:", r_sq)
print("Steigung linearer Trend: ", model.coef_)
print("Y-Achsenabschnitt linearer Trend: ", model.intercept_)

year_complete = year + year_future
trend_data = []
for i in year_complete:
  trend_data.append(model.coef_ * i + model.intercept_)

data_trend = ColumnDataSource(data = {
  "year": year_complete,
  "CO2": trend_data,
  "type": ["Trend, gesamt"] * 43
  })

# remaining budget for Münster's citizens from 2019 onwards (see Calc-sheet for calculation)
# paris_budget = 15242.7375718438
slope_paris = -117.8

paris_data = []
for i in year_future:
  paris_data.append(slope_paris * (i-2018) + data_real.data["CO2"][9])

paris_data_greater0 = [i for i in paris_data if i >= 0]
print("Prüfwert für Parisbudget; 'ausgegebenes Budget': ", sum(paris_data_greater0) - 1954) # 2018-data (1954) is already excluded from budget

data_paris = ColumnDataSource(data = {
  "year": year_future,
  "CO2": paris_data_greater0 + [-48] + ([math.nan] * 15),
  "type": ["Parisziele, gesamt"] * 33
  })

print(paris_data)
print(data_paris.data["CO2"])

percentage_real = [x / data_real.data["CO2"][0] for x in data_real.data["CO2"]]
data_real.add(name = "percentage", data = percentage_real)

percentage_warmth_real = [x / data_warmth_real.data["CO2"][0] for x in data_warmth_real.data["CO2"]]
data_warmth_real.add(name = "percentage", data = percentage_warmth_real)

percentage_electricity_real = [x / data_electricity_real.data["CO2"][0] for x in data_electricity_real.data["CO2"]]
data_electricity_real.add(name = "percentage", data = percentage_electricity_real)

percentage_traffic_real = [x / data_traffic_real.data["CO2"][0] for x in data_traffic_real.data["CO2"]]
data_traffic_real.add(name = "percentage", data = percentage_traffic_real)

percentage_planned = [x / data_real.data["CO2"][0] for x in data_planned.data["CO2"]]
data_planned.add(name = "percentage", data = percentage_planned)

percentage_trend = [x / data_real.data["CO2"][0] for x in data_trend.data["CO2"]]
data_trend.add(name = "percentage", data = percentage_trend)

percentage_paris = [x / data_real.data["CO2"][0] for x in data_paris.data["CO2"]]
data_paris.add(name = "percentage", data = percentage_paris)


# output to static HTML file
output_file("temp.html")

TOOLTIPS = [
    ("Jahr", "@year"),
    ("CO2 (tausend Tonnen)", "@CO2{0.00}"),
    ("Prozent von 1990", "@percentage{0.0%}"),
    ("Typ", "@type"),
]

p = figure(title = "Realität und Ziele", tooltips = TOOLTIPS,
            x_axis_label = 'Jahr', y_axis_label = 'CO2 (in tausend Tonnen)',
            y_range = (0, 2550),
            width=1000, height=500, sizing_mode = 'scale_width')

# ~ p.hover.mode = "hline"

# reality
p.line(source = data_real, x = "year", y = "CO2",
        legend_label = "CO2-Emissionen, gesamt",
        line_width = 2, color = "#d95f02")
p.line(source = data_warmth_real, x = "year", y = "CO2",
        legend_label = "CO2-Emissionen, Wärme",
        line_width = 2, color = "orange")
p.line(source = data_electricity_real, x = "year", y = "CO2",
        legend_label = "CO2-Emissionen, Strom",
        line_width = 2, color = "black")
p.line(source = data_traffic_real, x = "year", y = "CO2",
        legend_label = "CO2-Emissionen, Verkehr",
        line_width = 2, color = "brown")

# trend
p.line(source = data_trend, x = "year", y = "CO2",
        legend_label = "linearer Trend, gesamt",
        line_dash = "dotted", line_width = 2, color = "red")

# plans
p.line(source = data_planned, x = "year", y = "CO2",
        legend_label = "Münsteraner Ziele, gesamt",
        line_dash = "dashed", line_width = 2, color = "blue")
p.line(source = data_paris, x = "year", y = "CO2",
        legend_label = "Parisziele, gesamt",
        line_dash = "dashed", line_width = 2, color = "#1b9e77")

p.legend.location = "top_right"
p.title.text_font_size = "30pt"
p.legend.label_text_font_size = "15pt"
p.xaxis.axis_label_text_font_size = "15pt"
p.yaxis.axis_label_text_font_size = "15pt"
p.xaxis.major_label_text_font_size = "10pt"
p.yaxis.major_label_text_font_size = "10pt"


script, div = components(p, wrap_script = False)

# write js file
print(script,  file = open("plot.js", "w"))
# ~ # print div; for now needs to be manually added to index.html:
print("Folgendes <div> bitte manuell in der index.html ersetzen:")
print(div)

# show the results
show(p)
