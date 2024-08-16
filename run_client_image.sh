#!/bin/bash
USER_NAME=jovyan
SRC_CONTAINER=/home/$USER_NAME/workspace/src
SRC_HOST="$(pwd)"/client/src
CLIP_SRC_HOST="$(pwd)"/clip_nerf
CLIP_SRC_CONTAINER=/home/$USER_NAME/workspace/src/clip_nerf
DIR_NAME=$(dirname "$PWD")

docker run \
  -it \
  --name inference-server-client \
  --privileged \
  --rm \
  --net host \
  --ipc host \
  -e DISPLAY="$DISPLAY" \
  --volume="/dev:/dev":rw \
  --volume="$SRC_HOST":$SRC_CONTAINER \
  --volume="$CLIP_SRC_HOST":$CLIP_SRC_CONTAINER \
  --volume=$DIR_NAME/shared_docker_volume:/home/$USER_NAME/data:rw \
  thesis/inference-server-client:tf-v2.11.0