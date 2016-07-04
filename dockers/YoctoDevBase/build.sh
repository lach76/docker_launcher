#!/bin/bash
docker build -t 10.0.218.196:5000/yocto_devbase:ubuntu14.04 .
docker push 10.0.218.196:5000/yocto_devbase:ubuntu14.04
