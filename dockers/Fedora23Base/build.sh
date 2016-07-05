#!/bin/bash
docker build -t fedora.base:23 .
docker tag fedora.base:23 10.0.218.196:5000/fedora.base:23
docker push 10.0.218.196:5000/fedora.base:23
