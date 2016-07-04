#!/bin/bash
docker build -t yocto.dev.ubuntu.base:14.04 .
docker tag yocto.dev.ubuntu.base:14.04 10.0.218.196:5000/yocto.dev.ubuntu.base:14.04
docker push 10.0.218.196:5000/yocto.dev.ubuntu.base:14.04
