#!/bin/bash
docker build -t fedora.23.dev .
docker tag fedora.23.dev 10.0.218.196:5000/fedora.23.dev
docker push 10.0.218.196:5000/fedora.23.dev
