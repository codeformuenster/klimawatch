#!/bin/bash

docker run --rm -it -v $(pwd):/klimawatch conda:klimawatch /bin/bash -lc "conda activate klimawatch && cd /klimawatch && python generate_plots.py $@"
