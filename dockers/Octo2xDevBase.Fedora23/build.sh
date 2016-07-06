#!/bin/bash
docker build -t fedora.23.dev:octo2x .
docker tag fedora.23.dev:octo2x 10.0.218.196:5000/fedora.23.dev:octo2x
docker push 10.0.218.196:5000/fedora.23.dev:octo2x
