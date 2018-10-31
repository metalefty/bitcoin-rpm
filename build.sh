#!/bin/sh
docker run --interactive --tty --volume=${PWD}:/btcbuild amazonlinux:2 bash -c "cd /btcbuild && ./docker.sh"
