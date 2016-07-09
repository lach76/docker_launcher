#!/bin/bash
docker build -t ubuntu.14.04.dev:yocto .
docker tag ubuntu.14.04.dev:yocto 10.0.218.196:5000/ubuntu.14.04.dev:yocto
docker push 10.0.218.196:5000/ubuntu.14.04.dev:yocto
