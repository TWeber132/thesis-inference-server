#!/bin/bash

uid=$(eval "id -u")
gid=$(eval "id -g")
python_version="3.10.12"

docker build \
  --build-arg PYTHON_VERSION="$python_version" \
  --build-arg UID="$uid" \
  --build-arg GID="$gid" \
  --build-arg PASSWORD="$password" \
  -f client.Dockerfile \
  -t thesis/inference-server-client:tf-v2.11.0 .