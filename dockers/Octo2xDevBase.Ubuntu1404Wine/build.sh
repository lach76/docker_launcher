#!/bin/bash
docker build -t octo2x.dev.wine.ubuntu.base:14.04 .
docker tag octo2x.dev.wine.ubuntu.base:14.04 10.0.218.196:5000/octo2x.dev.wine.ubuntu.base:14.04
docker push 10.0.218.196:5000/octo2x.dev.wine.ubuntu.base:14.04