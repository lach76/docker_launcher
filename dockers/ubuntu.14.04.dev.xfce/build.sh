#!/bin/bash
docker build -t ubuntu.14.04.dev.xfce .
docker tag ubuntu.14.04.dev.xfce 10.0.218.196:5000/ubuntu.14.04.dev.xfce
docker push 10.0.218.196:5000/ubuntu.14.04.dev.xfce
