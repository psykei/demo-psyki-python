#!/bin/sh
VERSION=`python setup.py get_project_version | tail -n 1`
docker build -t pikalab/demo-psyki-python:latest-apple-m1 .
docker tag pikalab/demo-psyki-python:latest-apple-m1 pikalab/demo-psyki-python:$VERSION-apple-m1
docker push pikalab/demo-psyki-python:latest-apple-m1
docker push pikalab/demo-psyki-python:$VERSION-apple-m1
