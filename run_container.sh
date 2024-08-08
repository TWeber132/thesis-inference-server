#!/bin/bash

SRC_CONTAINER=/home/robot/workspace/src
SRC_HOST="$(pwd)"/src

docker run \
  -it \
  --name fastapi-server \
  --privileged \
  --rm \
  --net host \
  --ipc host \
  -e DISPLAY="$DISPLAY" \
  --volume="/dev:/dev":rw \
  --volume="$SRC_HOST":$SRC_CONTAINER \
  fastapi-server:3.10.12