#!/bin/bash

ENV_NAME="transforms"
PYTHON_VERSION="3.11"

conda create -n $ENV_NAME python=$PYTHON_VERSION -y

conda activate $ENV_NAME

pip install pygame

