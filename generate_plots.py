# coding=utf-8

import json  # writing json
import math
import sys  # reading command line arguments
import textwrap  # wrapping long lines
from pathlib import Path
from typing import Dict, Tuple

import numpy as np  # make it easier with numeric values
import pandas as pd
import plotly.graph_objects as go  # plots
from scipy.stats import linregress  # for computing the trend


def read_data() -> Tuple[pd.DataFrame, str]:
    # read data
    if len(sys.argv) <= 1:
        print("No city given, plotting data for Münster ('data/muenster.csv')")
        city = "muenster"
        df = pd.read_csv("data/muenster.csv")
    else:
        print("Plotting data for " + sys.argv[1])
        city = sys.argv[1]
        try:
            df = pd.read_csv("data/" + city + ".csv")

            if len(sys.argv) > 2:
                year = int(sys.argv[2])
                df = df.loc[df.year >= year]
        except:
            print(
                "File not found (or error in file). Does the file data/"
                + city
                + ".csv",
                "exist? Is it valid?",
            )
            exit(1)

    return df, city


def compute_start_years(df: pd.DataFrame) -> Dict[str, int]:
    start_year = {}
    # look for category-wise start_year
    for cat in set(df.category):
        if cat == "Einwohner":
            continue

        start_year[str(cat)] = df.loc[
            (df.category == cat) & (df.type == "real"), "year"
        ].min()

    return start_year


def calculate_features(df: pd.DataFrame):
    start_year = compute_start_years(df)

    emission_start = {}
    # compute category-wise percentage (compared to start)
    for cat in set(df.category):
        if cat != "Einwohner":
            emission_start[str(cat)] = df[
                (df.category == cat)
                & (df.year == start_year[cat])
                & (df.type == "real")
            ].co2.values[0]
            df.loc[df.category == cat, "percentage"] = (
                df[df.category == cat].co2.astype(float) / emission_start[str(cat)]
            )

    # compute trend based on current "Gesamt" data
    subdf_gesamt = df[df.category == "Gesamt"]
    subdf_gesamt_real = subdf_gesamt[subdf_gesamt.type == "real"]

    if len(subdf_gesamt) == 0 or len(subdf_gesamt_real) == 0:
        raise ValueError(
            "The data is missing entries in a category 'Gesamt' with type 'real'. Please add them."
        )

    trend_plot_name = "Trend"

    # compute trend beginning later than 1990 (if user wants it because data are missing)
    if len(sys.argv) == 3:
        print("Computing trend from", sys.argv[2], "onwards")
        subdf_gesamt_real = subdf_gesamt_real[subdf_gesamt_real.year > int(sys.argv[2])]
        trend_plot_name = "Trend (ab " + sys.argv[2] + ")"

    slope, intercept, r, p, stderr = linregress(
        subdf_gesamt_real.year, subdf_gesamt_real.co2
    )
    # print info about trend
    print(
        "linearer Trend: Steigung: ",
        slope,
        "Y-Achsenabschnitt: ",
        intercept,
        "R^2: ",
        r,
    )

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
    paris_budget_per_capita_from_jan_2019 = (
        paris_budget_germany_from_jan_2019 / inhabitants_germany
    )
    # take last 'Einwohner'-entry as reference
    paris_budget_full_city_from_jan_2019 = (
        paris_budget_per_capita_from_jan_2019 * df[df.type == "Einwohner"].iloc[-1].co2
    )

    # substract individual CO2 use; roughly 40%, see https://uba.co2-rechner.de/
    paris_budget_wo_individual_city_from_jan_2019 = (
        paris_budget_full_city_from_jan_2019 * 0.6
    )

    # substract already emitted CO2 from 2019 onwards
    # that is: emissions from 2019 and 2020
    # data for these years are most likely not available so we use the trend data for 2019 and 2020

    last_emissions_year = df[df.note == "last_emissions"].year.values

    if last_emissions_year < 2019:  # use trend data, no real data given
        emissions_2019 = slope * 2019 + intercept
        emissions_2020 = slope * 2020 + intercept
        emissions_2021 = slope * 2021 + intercept
        print(
            "No emission data for 2019 given, using trend data for 2019: ",
            emissions_2019,
        )
        print(
            "No emission data for 2020 given, using trend data for 2020: ",
            emissions_2020,
        )
        print(
            "No emission data for 2021 given, using trend data for 2021: ",
            emissions_2021,
        )
    elif last_emissions_year == 2019:
        emissions_2019 = last_emissions
        emissions_2020 = slope * 2020 + intercept
        emissions_2021 = slope * 2021 + intercept
        print(
            "No emission data for 2020 given, using trend data for 2020: ",
            emissions_2020,
        )
        print(
            "No emission data for 2021 given, using trend data for 2021: ",
            emissions_2021,
        )
    elif last_emissions_year == 2020:
        emissions_2019 = subdf_gesamt_real[subdf_gesamt_real.year == 2019].co2.values
        emissions_2020 = last_emissions
        emissions_2021 = slope * 2021 + intercept
        print(
            "No emission data for 2021 given, using trend data for 2020: ",
            emissions_2021,
        )
    elif last_emissions_year == 2021:
        emissions_2019 = subdf_gesamt_real[subdf_gesamt_real.year == 2019].co2.values
        emissions_2020 = subdf_gesamt_real[subdf_gesamt_real.year == 2020].co2.values
        emissions_2021 = last_emissions

    paris_budget_wo_individual_city_from_jan_2022 = (
        paris_budget_wo_individual_city_from_jan_2019 - emissions_2019 - emissions_2020 - emissions_2021
    )

    # compute slope for linear reduction of paris budget
    # We know the starting point b (in 2022), the area under the curve (remaining budget) and the function (m*x + b), but not the end point
    # solve for m / slope to get a linear approximation
    paris_slope = (-pow(emissions_2021, 2)) / (
        2 * paris_budget_wo_individual_city_from_jan_2022
    )
    years_to_climate_neutral = -emissions_2021 / paris_slope
    full_years_to_climate_neutral = int(np.round(years_to_climate_neutral[0]))

    # add final year of paris budget to trend data, if it is not included yet
    paris_target_year = 2022 + full_years_to_climate_neutral
    trend_years = subdf_gesamt_real.year.copy()
    if trend_years.iloc[-1] < paris_target_year:
        trend_years.loc[trend_years.index[-1] + 1] = paris_target_year

    # plot paris line
    future = list(range(0, full_years_to_climate_neutral, 1))  # from 2022 to 2050
    future.append(float(years_to_climate_neutral[0]))
    future = pd.DataFrame(np.array(future), columns=["year"])

    return (
        trend_years,
        slope,
        intercept,
        trend_plot_name,
        emission_start,
        future,
        paris_slope,
        emissions_2020,
        subdf_gesamt_real,
        start_year,
    )


def create_emission_plot(
    df: pd.DataFrame,
    city: str,
    trend_years,
    slope,
    intercept,
    trend_plot_name,
    emission_start,
    paris_slope,
    emissions_2020,
    start_year,
):
    # load color definition
    with open("data/colors.json", "r") as color_filehandle:
        color_dict = json.loads(color_filehandle.read())

    # create plot
    fig = go.Figure()

    # this loop plots all categories present in the csv, if type is either "real" or "geplant"
    for cat in set(df.category):
        if cat == "Einwohner":
            continue

        subdf_cat = df[(df.category == cat)]
        subdf_cat_real = subdf_cat[subdf_cat.type == "real"]

        if cat.lower() in color_dict.keys():
            cat_color = color_dict[cat.lower()]
        else:
            print(
                f"Missing color definition for category {cat.lower()}. Add it to data/colors.json"
            )
            cat_color = color_dict["sonstiges"]

        # add the real part as solid lines and markers
        fig.add_trace(
            go.Scatter(
                x=subdf_cat_real.year,
                y=subdf_cat_real.co2,
                name=cat + ", real",
                mode="lines+markers",
                legendgroup=cat,
                text=subdf_cat_real.percentage,
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

        subdf_cat_planned = subdf_cat[subdf_cat.type == "geplant"]
        fig.add_trace(
            go.Scatter(
                x=subdf_cat_planned.year,
                y=subdf_cat_planned.co2,
                name=cat + ", geplant",
                mode="lines+markers",
                line=dict(dash="dash", color=cat_color),
                legendgroup=cat,
                text=subdf_cat_planned.percentage,
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

    # TODO: make df instead of (double) calculation inline?
    fig.add_trace(
        go.Scatter(
            x=future.year + 2022,
            y=paris_slope * future.year + emissions_2020,
            name="Paris berechnet",
            mode="lines+markers",
            line=dict(dash="dash", color=color_dict["paris"]),
            legendgroup="future",
            text=(paris_slope * future.year + emissions_2020)
            / emission_start["Gesamt"],
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
            x=[2022],
            y=[emission_start["Gesamt"] + (emission_start["Gesamt"] / 30)],
            mode="text",
            text="heute",
            hoverinfo="none",
            legendgroup="future",
            showlegend=False,
        )
    )

    # horizontal legend; vertical line at 2022
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
                type="line", x0=2022, y0=0, x1=2022, y1=emission_start["Gesamt"]
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


def compute_paris_budget_for_youdrawit(
    df: pd.DataFrame,
    subdf_gesamt_real,
    slope,
    intercept,
    paris_slope,
    future,
    emissions_2020,
    start_year,
):
    # write computed Paris budget to JSON file for you-draw-it
    paris_data = {"chart_id": "you-draw-it"}

    max_past_emission = df.loc[(df.type == "real"), "co2"].max()

    paris_data["chart"] = {
        "heading": "Wie sollte sich der CO2-Ausstoß entwickeln?",
        "lastPointShownAt": 2022,
        "y_unit": "kt",
        "yAxisMax": max_past_emission + 0.1 * max_past_emission,
        "data": [],
    }

    # past data
    if start_year["Gesamt"] > 1990:
        while start_year["Gesamt"] % 5 != 0:
            # go back in time (at most 4 years) to have a larger x-axis
            start_year["Gesamt"] = start_year["Gesamt"] - 1

    past = range(start_year["Gesamt"], 2022, 5)

    # variables to write to JSON later on
    years_past_total_real = list(subdf_gesamt_real.year)
    values_past_total_real = list(subdf_gesamt_real.co2)

    for y in past:
        try:
            yidx = years_past_total_real.index(y)
            paris_data["chart"]["data"].append({y: values_past_total_real[yidx]})
        except ValueError:
            print(
                "You-draw-it-chart: Emissions for",
                y,
                "unknown. Estimating from the trend.",
            )
            paris_data["chart"]["data"].append({y: slope * y + intercept})

    # years with remaining budget
    paris_years = future[:-1].year + 2022
    budget_per_year = paris_slope * future[:-1].year + emissions_2020

    for y in range(len(paris_years)):
        if y % 5 == 0:  # print only every 5th year
            paris_data["chart"]["data"].append(
                {int(paris_years[y]): budget_per_year[y]}
            )

    climate_neutral_by = int(np.round(max(paris_years)))
    # range every climate-neutral year, because
    # we don't know the climate-neutral year and can't do 5-year steps
    years_after_budget = range(climate_neutral_by + 1, 2051, 1)

    for y in years_after_budget:
        if y % 5 == 0:  # print only every 5th year
            paris_data["chart"]["data"].append({y: 0})

    with open(
        "hugo/data/you_draw_it_" + city + ".json", "w", encoding="utf8"
    ) as outfile:
        json.dump(paris_data, outfile, indent=2, ensure_ascii=False)


##############################################################
## Visualisation of status of modules of Klimaschutzkonzepte##
##############################################################


def create_collapsible(city):
    try:
        modules_df = pd.read_csv("data/" + city + "_sachstand.csv")
    except:
        print(
            "Sachstand file for "
            + city
            + " (data/"
            + city
            + "_sachstand.csv) not found. Not creating module plot."
        )
        exit(1)

    # build component tree
    components = {}
    for i, row in modules_df.iterrows():
        components[row["id"]] = row

    component_tree = {}
    first_order_ids = []
    last_order_ids = []
    for key, component in components.items():
        last_order_ids.append(component["id"])

        if component["parent"] is None or (
            type(component["parent"]) is float and math.isnan(component["parent"])
        ):
            component_tree[key] = []
            first_order_ids.append(component["id"])
        else:
            if component["parent"] not in component_tree.keys():
                component_tree[component["parent"]] = [key]
            else:
                component_tree[component["parent"]].append(key)

            if component["parent"] in last_order_ids:
                last_order_ids.remove(component["parent"])

    html_acc = "<div>"

    color_map = {
        "#01873B": "timeline-good",
        "#AE1B1B": "timeline-bad",
        "orange": "timeline-warn",
    }

    for key in first_order_ids:

        color = color_map.get(components[key]["assessment"], "")

        html_comp = (
            """
            <button type="button" class="collapsible """
            + color
            + """ ">"""
            + components[key]["title"]
            + """</button>
            <div class="content">
        """
        )

        for second_key in component_tree[key]:
            second_color = color_map.get(components[second_key]["assessment"], "")
            second_html_comp = (
                """
                <button type="button" class="collapsible """
                + second_color
                + """ ">"""
                + components[second_key]["title"]
                + """</button>
                <div class="content">
                <div class="row">
                <ul id="timeline" class="timeline">
                    <div class="arrowhead"></div>
                    """
            )

            for i, third_key in enumerate(reversed(component_tree[second_key])):
                third_color = color_map.get(components[third_key]["assessment"], "")
                if "plan" in components[third_key]["title"]:
                    year = "Plan"
                else:
                    year = "".join(
                        [x for x in components[third_key]["title"] if x.isnumeric()][
                            0:4
                        ]
                    )

                li_class = ""
                if i == 3:
                    li_class = "last"
                elif i == 1:
                    li_class = "timeline-inverted "

                third_html_comp = (
                    """
                    <li class=" """
                    + li_class
                    + """ ">
                        <div class="timeline-badge">"""
                    + year
                    + """ </div>
                        <div class="timeline-panel """
                    + third_color
                    + """ ">

                            <div class="timeline-heading">
                                <h3 class="timeline-title">"""
                    + components[third_key]["title"]
                    + """</h3>
                            </div>

                            <div class="timeline-body">
                                <p>
                                    """
                    + components[third_key]["text"]
                    + """
                                </p>
                            </div>

                        </div>
                    </li>
                """
                )

                if i == 3:
                    third_html_comp = (
                        '<div style="clear: both"></div>\n' + third_html_comp
                    )

                second_html_comp += third_html_comp

            second_html_comp += "</div></ul></div>"

            html_comp += second_html_comp

        html_comp += "</div>"

        html_acc += html_comp + "\n"

    html_acc += """
        <script>
            var coll = document.getElementsByClassName("collapsible");
            var i;

            for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.display === "block") {
                        content.style.display = "none";
                    } else {
                        content.style.display = "block";
                    }
                });
            }
        </script>
        </div>
    """

    with open(
        Path(f"hugo/layouts/shortcodes/modules_{city}.html"), "w", encoding="utf-8"
    ) as fp:
        fp.write(html_acc)


if __name__ == "__main__":
    df, city = read_data()

    (
        trend_years,
        slope,
        intercept,
        trend_plot_name,
        emission_start,
        future,
        paris_slope,
        emissions_2020,
        subdf_gesamt_real,
        start_year,
    ) = calculate_features(df=df)

    create_emission_plot(
        df=df,
        city=city,
        trend_years=trend_years,
        slope=slope,
        intercept=intercept,
        trend_plot_name=trend_plot_name,
        emission_start=emission_start,
        paris_slope=paris_slope,
        emissions_2020=emissions_2020,
        start_year=start_year,
    )

    compute_paris_budget_for_youdrawit(
        df=df,
        subdf_gesamt_real=subdf_gesamt_real,
        slope=slope,
        intercept=intercept,
        paris_slope=paris_slope,
        future=future,
        emissions_2020=emissions_2020,
        start_year=start_year,
    )

    create_collapsible(city)
