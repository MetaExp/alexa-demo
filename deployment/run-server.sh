#!/bin/bash
docker stop alexa-container
docker rm alexa-container
docker run --name alexa-container \
           --publish=${1:-8000}:8000 \
           -d \
	       -e "METAEXP_DEV=true"\
           server
