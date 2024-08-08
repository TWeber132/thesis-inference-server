#!/bin/bash
##############################################################################
##                            Build the image                               ##
##############################################################################
docker build \
  -f inference_server.Dockerfile \
  -t thesis/inference-server:tf-v2.11.0 .

