#!/bin/bash
docker build -t ubuntu.14.04.dev.xfce:octo2x .
docker tag ubuntu.14.04.dev.xfce:octo2x 10.0.218.196:5000/ubuntu.14.04.dev.xfce:octo2x
docker push 10.0.218.196:5000/ubuntu.14.04.dev.xfce:octo2x
