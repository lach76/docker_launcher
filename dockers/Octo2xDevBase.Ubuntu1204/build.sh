#!/bin/bash
docker build -t 10.0.218.196:5000/octo2x_devbase:ubuntu12.04 .
docker push 10.0.218.196:5000/octo2x_devbase:ubuntu12.04