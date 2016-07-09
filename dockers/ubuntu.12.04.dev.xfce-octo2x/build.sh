#!/bin/bash
docker build -t ubuntu.12.04.dev.xfce:octo2x .
docker tag ubuntu.12.04.dev.xfce:octo2x 10.0.218.196:5000/ubuntu.12.04.dev.xfce:octo2x
docker push 10.0.218.196:5000/ubuntu.12.04.dev.xfce:octo2x
