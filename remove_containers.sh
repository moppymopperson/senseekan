#!/usr/bin/env bash

# Stop all the containers
docker stop senseekan streamer senseekan-server

# Remove all the containers
docker rm senseekan streamer senseekan-server
