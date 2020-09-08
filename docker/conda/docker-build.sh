#!/bin/bash

cp ../../environment.yml .
docker build -t conda:klimawatch .
rm environment.yml 