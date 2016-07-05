#!/bin/bash
docker build -t octo2x.dev.fedora.base:23 .
docker tag octo2x.dev.fedora.base:23 10.0.218.196:5000/octo2x.dev.fedora.base:23
docker push 10.0.218.196:5000/octo2x.dev.fedora.base:23
