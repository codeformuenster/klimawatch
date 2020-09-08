#!/bin/bash

DOCKER_IMAGE=klakegg/hugo:0.59.1-busybox

docker run --rm -it -p 1313:1313 -v $(pwd)/hugo:/src ${DOCKER_IMAGE} $@