# coding=utf-8

import json  # writing json
import os  # possibility to delete files
import sys  # reading command line arguments
import textwrap  # wrapping long lines

import numpy as np  # make it easier with numeric values
import pandas
import plotly.graph_objects as go  # plots
from scipy.stats import linregress  # for computing the trend

# read data
if len(sys.argv) <= 1:

    print("No city given, plotting data for Münster ('data/muenster.csv')")
    city = "muenster"
    df = pandas.read_csv("data/muenster.csv")
else:
    print("Plotting data for " + sys.argv[1])
    city = sys.argv[1]
    try:
        df = pandas.read_csv("data/" + city + ".csv")
    except:
        print(
            "File not found (or error in file). Does the file data/" + city + ".csv",
            "exist? Is it valid?",
        )
        exit(1)

with open("data/colors.json", "r") as color_filehandle:
    color_dict = json.loads(color_filehandle.read())

# create plot
fig = go.Figure()

start_year = {}
# look for category-wise start_year
for cat in set(df.category):
    if cat == "Einwohner":
        continue

    start_year[str(cat)] = df.loc[
        (df.category == cat) & (df.type == "real"), "year"
    ].min()

emission_start = {}
# compute category-wise percentage (compared to start)
for cat in set(df.category):
    if cat != "Einwohner":
        emission_start[str(cat)] = df[
            (df.category == cat) & (df.year == start_year[cat]) & (df.type == "real")
        ].co2.values[0]
        df.loc[df.category == cat, "percentage"] = (
            df[df.category == cat].co2.astype(float) / emission_start[str(cat)]
        )

# set() only lists unique values
# this loop plots all categories present in the csv, if type is either "real" or "geplant"
for cat in set(df.category):
    if cat == "Einwohner":
        continue

    subdf = df[(df.category == cat)]

    subdf_real = subdf[subdf.type == "real"]

    if cat.lower() in color_dict.keys():
        cat_color = color_dict[cat.lower()]
    else:
        print(
            "Missing color definition for category {cat.lower()}. Add it to data/colors.json"
        )
        cat_color = color_dict["sonstiges"]

    # add the real part as solid lines and markers
    fig.add_trace(
        go.Scatter(
            x=subdf_real.year,
            y=subdf_real.co2,
            name=cat + ", real",
            mode="lines+markers",
            legendgroup=cat,
            text=subdf_real.percentage,
            line=dict(color=cat_color),
            hovertemplate="<b>tatsächliche</b> Emissionen, Kategorie: "
            + cat
            + "<br>Jahr: %{x}<br>"
            + "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>"
            + "Prozent von Emissionen "
            + str(start_year[cat])
            + ": %{text:.0%}"
            + "<extra></extra>",
        )  # no additional legend text in tooltip
    )

    subdf_planned = subdf[subdf.type == "geplant"]
    fig.add_trace(
        go.Scatter(
            x=subdf_planned.year,
            y=subdf_planned.co2,
            name=cat + ", geplant",
            mode="lines+markers",
            line=dict(dash="dash", color=cat_color),
            legendgroup=cat,
            text=subdf_planned.percentage,
            hovertemplate="<b>geplante</b> Emissionen, Kategorie: "
            + cat
            + "<br>Jahr: %{x}<br>"
            + "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>"
            + "Prozent von Emissionen "
            + str(start_year[cat])
            + ": %{text:.0%}"
            + "<extra></extra>",
        )  # no additional legend text in tooltip
    )

# compute trend based on current "Gesamt" data
subdf = df[df.category == "Gesamt"]
subdf_real = subdf[subdf.type == "real"]

if len(subdf) == 0 or len(subdf_real) == 0:
    raise ValueError(
        "The data is missing entries in a category 'Gesamt' with type 'real'. Please add them."
    )

# variables to write to JSON later on
years_past_total_real = list(subdf_real.year)
values_past_total_real = list(subdf_real.co2)

trend_plot_name = "Trend"

# compute trend beginning later than 1990 (if user wants it because data are missing)
if len(sys.argv) == 3:
    print("Computing trend from", sys.argv[2], "onwards")
    subdf_real = subdf_real[subdf_real.year > int(sys.argv[2])]
    trend_plot_name = "Trend (ab " + sys.argv[2] + ")"

slope, intercept, r, p, stderr = linregress(subdf_real.year, subdf_real.co2)
# print info about trend
print("linearer Trend: Steigung: ", slope, "Y-Achsenabschnitt: ", intercept, "R^2: ", r)


# compute remaining paris budget
last_emissions = df[df.note == "last_emissions"].co2.values

if len(last_emissions) == 0:
    print(
        "No 'last_emissions' keyword found. You need to mark the last measured total emission with this keyword in the note column. Exiting."
    )
    exit()
else:
    last_emissions = last_emissions[0]

# see https://scilogs.spektrum.de/klimalounge/wie-viel-co2-kann-deutschland-noch-ausstossen/
# remaining budget for germany from beginning 2019 onwards
paris_budget_germany_from_jan_2019 = 7300000
inhabitants_germany = 83019213
paris_budget_per_capita_from_jan_2019 = paris_budget_germany_from_jan_2019 / inhabitants_germany
# take last 'Einwohner'-entry as reference
paris_budget_full_city_from_jan_2019 = (
    paris_budget_per_capita_from_jan_2019 * df[df.type == "Einwohner"].iloc[-1].co2
)

# substract individual CO2 use; roughly 40%, see https://uba.co2-rechner.de/
paris_budget_wo_individual_city_from_jan_2019 = paris_budget_full_city_from_jan_2019 * 0.6

# substract already emitted CO2 from 2019 onwards
# that is: emissions from 2019 and 2020
# data for these years are most likely not available so we use the trend data for 2019 and 2020

last_emissions_year = df[df.note == "last_emissions"].year.values

if last_emissions_year < 2019: # use trend data, no real data given
    emissions_2019 = slope * 2019 + intercept
    emissions_2020 = slope * 2020 + intercept
    print("No emission data for 2019 given, using trend data for 2019: ", emissions_2019)
    print("No emission data for 2020 given, using trend data for 2020: ", emissions_2020)
elif last_emissions_year == 2019:
    emissions_2019 = last_emissions
    emissions_2020 = slope * 2020 + intercept
    print("No emission data for 2020 given, using trend data for 2020: ", emissions_2020)
elif last_emissions_year == 2020:
    emissions_2019 = subdf_real[subdf_real.year == 2019]
    emissions_2020 = last_emissions

paris_budget_wo_individual_city_from_jan_2021 = (
    paris_budget_wo_individual_city_from_jan_2019 - emissions_2019 - emissions_2020
)

# compute slope for linear reduction of paris budget
# We know the starting point b (in 2021), the area under the curve (remaining budget) and the function (m*x + b), but not the end point
# solve for m / slope to get a linear approximation
paris_slope = (-pow(emissions_2020, 2)) / (2 * paris_budget_wo_individual_city_from_jan_2021)
years_to_climate_neutral = -emissions_2020 / paris_slope
full_years_to_climate_neutral = int(np.round(years_to_climate_neutral))

# add final year of paris budget to trend data, if it is not included yet
paris_target_year = 2021 + full_years_to_climate_neutral
trend_years = subdf.year.copy()
if trend_years.iloc[-1] < paris_target_year:
    trend_years.loc[trend_years.index[-1] + 1] = paris_target_year

# plot trend
fig.add_trace(
    go.Scatter(
        x=trend_years,
        y=slope * trend_years + intercept,
        name=trend_plot_name,
        mode="lines",
        line=dict(dash="dot", color=color_dict["trend"]),
        legendgroup="future",
        text=(slope * trend_years + intercept) / emission_start["Gesamt"],
        hovertemplate="<b>bisheriger "
        + trend_plot_name
        + "</b>"
        + "<br>Jahr: %{x}<br>"
        + "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>"
        + "Prozent von Emissionen "
        + str(start_year["Gesamt"])
        + ": %{text:.0%}"
        + "<extra></extra>",
    )  # no additional legend text in tooltip
)

# plot paris line
future = list(range(0, full_years_to_climate_neutral, 1))  # from 2021 to 2050
future.append(float(years_to_climate_neutral))
future = pandas.DataFrame(np.array(future), columns=["year"])

# TODO: make df instead of (double) calculation inline?
fig.add_trace(
    go.Scatter(
        x=future.year + 2021,
        y=paris_slope * future.year + emissions_2020,
        name="Paris berechnet",
        mode="lines+markers",
        line=dict(dash="dash", color=color_dict["paris"]),
        legendgroup="future",
        text=(paris_slope * future.year + emissions_2020) / emission_start["Gesamt"],
        hovertemplate="<b>Paris-Budget</b>"
        + "<br>Jahr: %{x:.0f}<br>"
        + "CO<sub>2</sub>-Emissionen (tausend Tonnen): %{y:.1f}<br>"
        + "Prozent von Gesamt-Emissionen "
        + str(start_year["Gesamt"])
        + ": %{text:.0%}"
        + "<extra></extra>",
    )  # no additional legend text in tooltip
)

fig.add_trace(
    go.Scatter(
        x=[2021],
        y=[emission_start["Gesamt"] + (emission_start["Gesamt"] / 30)],
        mode="text",
        text="heute",
        hoverinfo="none",
        legendgroup="future",
        showlegend=False,
    )
)

# horizontal legend; vertical line at 2021
fig.update_layout(
    title="Realität und Ziele",
    yaxis_title="CO<sub>2</sub> in tausend Tonnen",
    xaxis_title="Jahr",
    # horizontal legend
    legend_orientation="h",
    # put legend above plot to avoid overlapping-bug
    legend_xanchor="center",
    legend_y=-0.25,
    legend_x=0.5,
    legend_font_size=10,
    # disable dragmode for better mobile experience
    dragmode=False,
    # German number separators
    separators=",.",
    # vertical "today" line
    shapes=[
        go.layout.Shape(
            type="line", x0=2021, y0=0, x1=2021, y1=emission_start["Gesamt"]
        )
    ],
)

# write plot to file
fig.write_html(
    "hugo/layouts/shortcodes/paris_" + city + ".html",
    include_plotlyjs=False,
    config={"displayModeBar": False},
    full_html=False,
    auto_open=True,
)

# write computed Paris budget to JSON file for you-draw-it
paris_data = {}

paris_data = {}

paris_data["chart_id"] = "you-draw-it"

max_past_emission = df.loc[(df.type == "real"), "co2"].max()

paris_data["chart"] = {
    "heading": "Wie sollte sich der CO2-Ausstoß entwickeln?",
    "lastPointShownAt": 2021,
    "y_unit": "kt",
    "yAxisMax": max_past_emission + 0.1 * max_past_emission,
    "data": [],
}

# past data

if start_year["Gesamt"] > 1990:
    while start_year["Gesamt"] % 5 != 0:
        # go back in time (at most 4 years) to have a larger x-axis
        start_year["Gesamt"] = start_year["Gesamt"] - 1

past = range(start_year["Gesamt"], 2021, 5)

for y in past:
    try:
        yidx = years_past_total_real.index(y)
        paris_data["chart"]["data"].append({y: values_past_total_real[yidx]})
    except ValueError:
        print(
            "You-draw-it-chart: Emissions for", y, "unknown. Estimating from the trend."
        )
        paris_data["chart"]["data"].append({y: slope * y + intercept})

# years with remaining budget
paris_years = future[:-1].year + 2021
budget_per_year = paris_slope * future[:-1].year + emissions_2020

for y in range(len(paris_years)):
    if y % 5 == 0:  # print only every 5th year
        paris_data["chart"]["data"].append({int(paris_years[y]): budget_per_year[y]})

climate_neutral_by = int(np.round(max(paris_years)))
# range every climate-neutral year, because
# we don't know the climate-neutral year and can't do 5-year steps
years_after_budget = range(climate_neutral_by + 1, 2051, 1)

for y in years_after_budget:
    if y % 5 == 0:  # print only every 5th year
        paris_data["chart"]["data"].append({y: 0})

with open("hugo/data/you_draw_it_" + city + ".json", "w", encoding="utf8") as outfile:
    json.dump(paris_data, outfile, indent=2, ensure_ascii=False)

##############################################################
## Visualisation of status of modules of Klimaschutzkonzepte##
##############################################################
try:
    modules_df = pandas.read_csv("data/" + city + "_sachstand.csv")
except:
    print(
        "Sachstand file for "
        + city
        + " (data/"
        + city
        + "_sachstand.csv) not found. Not creating module plot."
    )
    exit(1)

# find unique overarching categories (here: first character of ID)
categories = set()
for c in modules_df["id"]:
    categories.add(c[0:1])

## create a single treemap plot for every overarching category

modules_df = modules_df.fillna("None")

# delete old plot file
os.remove("hugo/layouts/shortcodes/modules_" + city + ".html")
modules_plot_file = open("hugo/layouts/shortcodes/modules_" + city + ".html", "a")

for cat in categories:

    modules_onecat = modules_df[modules_df.id.str.startswith(cat)].copy()
    modules_onecat["potential"] = modules_onecat["potential"].astype(str)

    fig_modules = go.Figure(
        go.Treemap(
            branchvalues="remainder",
            ids=modules_onecat["id"],
            labels="<b>"
            + modules_onecat["title"]
            + "</b> ("
            + modules_onecat["id"]
            + ")",
            parents=modules_onecat["parent"],
            values=modules_onecat["priority"],
            marker_colors=modules_onecat["assessment"],
            text=(modules_onecat["text"]).apply(
                lambda txt: "<br>".join(textwrap.wrap(txt, width=100))
            ),
            textinfo="label+text",
            hovertext=(
                modules_onecat["text"] + " (" + modules_onecat["id"] + ")"
                "<br>Priorität: "
                + (modules_onecat["priority"]).astype(str)
                + "<br>Potential: "
                + (modules_onecat["potential"]).astype(str)
            ).apply(lambda txt: "<br>".join(textwrap.wrap(txt, width=100))),
            hoverinfo="text",
            pathbar={"visible": True},
            insidetextfont={"size": 75},
        )
    )

    fig_modules.update_layout(
        margin=dict(r=10, l=10)
        # ~ height = 750
    )

    modules_plot_file.write(
        fig_modules.to_html(
            include_plotlyjs=False, config={"displayModeBar": False}, full_html=False
        )
    )


modules_plot_file.close()
