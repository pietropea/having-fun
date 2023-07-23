#!/bin/bash

##### Bootstrap API dev environment
cd ./api
# Create the Python virtual env
python3 -m venv .venv
source .venv/bin/activate
# Install project dependencies
pip install -r ./requirements-dev.txt
pip install -r ./requirements.txt
deactivate
cd ..

##### Bootstrap UI dev environment
cd ./ui
yarn
cd ..

# Install the pre-commit hook
python3 -m venv .venv
source .venv/bin/activate
pip install -r ./api/requirements-dev.txt
pre-commit install