#!/bin/bash
docker build -t ubuntu.14.04.dev .
docker tag ubuntu.14.04.dev 10.0.218.196:5000/ubuntu.14.04.dev
docker push 10.0.218.196:5000/ubuntu.14.04.dev
