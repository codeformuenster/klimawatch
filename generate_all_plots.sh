#!/usr/bin/env bash
for city in muenster hamburg karlsruhe koeln landau leipzig
do
    python generate_plots.py $city
done
