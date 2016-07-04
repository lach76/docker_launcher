#!/bin/bash
docker build -t 10.0.218.196:5000/octo2x_devbase:ubuntu14.04.wine .
docker push 10.0.218.196:5000/octo2x_devbase:ubuntu14.04.wine
