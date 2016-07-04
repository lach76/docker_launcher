#!/bin/bash
docker build -t 10.0.218.196:5000/ubuntu1404:base .
docker push 10.0.218.196:5000/ubuntu1404:base
