#!/bin/bash

SRC_CONTAINER=/home/robot/workspace/src
SRC_HOST="$(pwd)"/client/src

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
  thesis/inference-server-client:tf-v2.11.0