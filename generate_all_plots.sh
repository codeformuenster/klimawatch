#!/usr/bin/env bash
for city in muenster hamburg karlsruhe koeln landau leipzig moers
do
    if test "$city" == "karlsruhe"
    then
        python generate_plots.py $city 2007
    else
        python generate_plots.py $city
    fi
done
