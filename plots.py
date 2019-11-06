import math
import fileinput

import numpy as np
from sklearn.linear_model import LinearRegression

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components

year = [1990, 1995, 2000, 2005, 2006, 2010, 2011, 2015, 2016, 2017]
year_future = [2018, 2019, 2020,
                2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,
                2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039,
                2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050]

data_real = ColumnDataSource(data = {
  "year": year,
  "CO2": [2517, 2459, 2471, 2386, 2295, 2116, 2061, 2017, 1981, 1954],
  "type": ["real"] * 10
  })


year_complete = year + year_future

data_planned = ColumnDataSource(data = {
  "year": year_complete,
  "CO2": [2517, 2349.2, 2181.4, 2013.6, 1980.04, 1845.8, 1812.24, 1678, 1644.44, 1610.88, 1577.32, 1543.76, 1510.2,
          1281.5725, 1241.72, 1201.8675, 1162.015, 1122.1625, 1082.31, 1042.4575, 1002.605, 962.7525,
          922.9, 883.0475, 843.195, 803.3425, 763.49, 723.6375, 683.785, 643.9325, 604.08, 564.2275,
          524.375, 484.5225, 444.67, 404.8175, 364.965, 325.1125, 285.26, 245.4075, 205.555, 165.7025,
          125.85],
  "type": ["geplant"] * 43
  })

# compute trend based on current data
year_r = np.array(year[0:10]).reshape(-1, 1)
data_r = data_real.data["CO2"][0:10]
model = LinearRegression().fit(year_r, data_r)

r_sq = model.score(year_r, data_r)
print('R^2 linearer Trend:', r_sq)

year_complete = year + year_future
trend_data = []
for i in year_complete:
  trend_data.append(model.coef_ * i + model.intercept_)

data_trend = ColumnDataSource(data = {
  "year": year_complete,
  "CO2": trend_data,
  "type": ["Trend"] * 43
  })

# remaining budget for Münster's citizens from 2019 onwards (see Calc-sheet for now for calculation)
paris_budget = 27304.5626197396

# TODO: proper calculation!
slope_paris = -72.5

paris_data = []
for i in year_future:
  paris_data.append(slope_paris * (i-2018) + data_real.data["CO2"][9])

print(slope_paris)
print(paris_data)
paris_data_greater0 = [i for i in paris_data if i >= 0]
print(paris_data_greater0)
print(sum(paris_data_greater0))

data_paris = ColumnDataSource(data = {
  "year": year_future,
  "CO2": paris_data,
  "type": ["Parisziele"] * 33
  })

percentage_real = [x / data_real.data["CO2"][0] for x in data_real.data["CO2"]]
data_real.add(name = "percentage", data = percentage_real)

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
    ("CO2 (tausend Tonnen)", "@CO2{0,00}"),
    ("Prozent von 1990", "@percentage{0.0%}"),
    ("Typ", "@type"),
]

p = figure(title = "Pläne und Realität", tooltips = TOOLTIPS,
            x_axis_label = 'Jahr', y_axis_label = 'CO2 (in tausend Tonnen)',
            y_range = (0, 2550), sizing_mode = 'scale_width')

p.hover.mode = "vline"

p.line(source = data_real, x = "year", y = "CO2", legend_label = "CO2-Emissionen (in tausend Tonnen)",
        line_width = 2, color = "#d95f02")
p.line(source = data_planned, x = "year", y = "CO2", legend_label = "CO2-Ziele (in tausend Tonnen)",
        line_width = 2, color = "#1b9e77")
p.line(source = data_trend, x = "year", y = "CO2", legend_label = "linearer Trend",
        line_width = 2, color = "red")
p.line(source = data_paris, x = "year", y = "CO2", legend_label = "nötig für Paris",
        line_width = 2, color = "blue")

p.legend.location = "center_left"
p.title.text_font_size = "30pt"
p.legend.label_text_font_size = "20pt"
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
# ~ show(p)
