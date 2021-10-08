#!/usr/bin/env bash
for city in muenster koeln leipzig hamburg karlsruhe landau moers chemnitz berlin_verursacherbilanz muenchen duesseldorf paderborn dortmund bielefeld ulm
do
    if test "$city" == "karlsruhe"
    then
        python generate_plots.py $city 2007
    else
        python generate_plots.py $city
    fi
done
