#!/bin/bash
##############################################################################
##                            Build the image                               ##
##############################################################################
docker build \
  -f server.Dockerfile \
  -t universalrobotcell1/inference-server:tf-v2.11.0 .

