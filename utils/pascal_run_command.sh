#!/bin/bash
sudo docker run \
--rm \
-v /media/ali/DATA/DATABASE/DCA/docker/pascal:/home/shared \
--net=host \
--env="DISPLAY" \
--volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
--publish 8888:8888 \
--privileged \
-it alialkadhim/pascal \
/bin/bash
