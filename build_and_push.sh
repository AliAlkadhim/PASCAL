#!/bin/bash
sudo docker build -t alialkadhim/pascal:1.0 .
docker tag alialkadhim/pascal:1.0 alialkadhim/pascal:1.0
docker push alialkadhim/pascal:1.0
