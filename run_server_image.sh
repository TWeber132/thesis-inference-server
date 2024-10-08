#!/bin/bash
##############################################################################
##                            Run the container                             ##
##############################################################################
BASE_NAME=$(basename "$PWD")
DIR_NAME=$(dirname "$PWD")
USER_NAME=jovyan

docker run \
  --name inference-server \
  --rm \
  -it \
  --net=host \
  -v $DIR_NAME/shared_docker_volume:/home/$USER_NAME/data:rw \
  -e DISPLAY="$DISPLAY" \
  --gpus all \
  universalrobotcell1/inference-server-wo:tf-v2.11.0
