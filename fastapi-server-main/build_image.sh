#!/bin/bash

uid=$(eval "id -u")
gid=$(eval "id -g")
password="proximity"
python_version="3.10.12"

docker build \
  --build-arg PYTHON_VERSION="$python_version" \
  --build-arg UID="$uid" \
  --build-arg GID="$gid" \
  --build-arg PASSWORD="$password" \
  -f Dockerfile \
  -t fastapi-server:"$python_version" .