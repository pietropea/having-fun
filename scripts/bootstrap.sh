#!/bin/bash

export PROJECT_ROOT=$(dirname $(git rev-parse --git-dir))

cd $PROJECT_ROOT/api

# Create the Python virtual env
python3 -m venv .venv
source .venv/bin/activate

# Install project dependencies
pip install -r $PROJECT_ROOT/app/requirements-dev.txt

# Install the pre-commit hook
pre-commit install