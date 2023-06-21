#!/bin/bash

sudo docker run \
--rm \
-v /home/ali/Desktop/Pulled_Github_Repositories/PASCAL:/home/PASCAL_REPO \
--net=host \
--env="DISPLAY" \
--volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
--publish 8888:8888 \
--privileged \
-it alialkadhim/pascal:latest \
/bin/bash
