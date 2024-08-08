#!/bin/bash
##############################################################################
##                            Run the container                             ##
##############################################################################
BASE_NAME=$(basename "$PWD")
DIR_NAME=$(dirname "$PWD")
USER_NAME=jovyan

docker run \
  --name tf \
  --rm \
  -it \
  --net=host \
  -v $DIR_NAME/shared_docker_volume:/home/$USER_NAME/data:rw \
  -e DISPLAY="$DISPLAY" \
  --gpus all \
  thesis/inference-server:tf-v2.11.0
