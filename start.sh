#!/bin/sh

docker build . -t docker-flask-app

docker run -p 5000:5000 docker-flask-app