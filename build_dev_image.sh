#!/bin/bash
##############################################################################
##                            Build the image                               ##
##############################################################################
docker build \
  -f dev.Dockerfile \
  -t thesis/inference-server-dev:tf-v2.11.0 .

