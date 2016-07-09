#!/bin/bash
docker build -t ubuntu.12.04.dev .
docker tag ubuntu.12.04.dev 10.0.218.196:5000/ubuntu.12.04.dev
docker push 10.0.218.196:5000/ubuntu.12.04.dev
