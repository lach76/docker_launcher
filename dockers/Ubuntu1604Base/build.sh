#!/bin/bash
docker build -t ubuntu.base:16.04 .
docker tag ubuntu.base:16.04 10.0.218.196:5000/ubuntu.base:16.04
docker push 10.0.218.196:5000/ubuntu.base:16.04
