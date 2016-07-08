#!/bin/bash
docker build -t ubuntu.14.04.dev:octo2x.wine  .
docker tag ubuntu.14.04.dev:octo2x.wine 10.0.218.196:5000/ubuntu.14.04.dev:octo2x.wine
docker push 10.0.218.196:5000/ubuntu.14.04.dev:octo2x.wine