#!/usr/bin/env bash

# This script creates a docker container that restarts automatically anytime
# it crashes and everytime the system reboots. This ensures that all you have
# to do to start Senseekan is give it power

# This command builds the image if you haven't built it already
docker build . -t senseekan

# --detach runs the container in the background
# --restart always makes the container run automatically
# --privileged is required to access GPIO
# --net=host is needed for bluetooth to work properly
# -v $pwd:/senseekan mounts the current directory
# --name senseekan specifies the name the container will be given
# senseekan is the image to use, the one we built just above this
# The last line is the command to run
docker run --detach \
	--restart=always \
	--privileged \
	--net=host \
	-v $(pwd):/senseekan \
	--name senseekan \
	senseekan \
	bash "-c" "cd /senseekan/src && python Senseekan.py" # Run the script
