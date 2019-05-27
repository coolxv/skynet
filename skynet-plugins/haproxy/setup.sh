#!/bin/bash

rm -rf venv;
pip install --upgrade setuptools > /dev/null 2>&1;
pip install --upgrade pip > /dev/null 2>&1;
pip install --upgrade virtualenv > /dev/null 2>&1;
virtualenv venv&&
source venv/bin/activate&&
venv/bin/pip install --upgrade setuptools > /dev/null 2>&1;
venv/bin/pip install --upgrade pip > /dev/null 2>&1;
venv/bin/pip install -r requirements.txt&&
nohup venv/bin/python -u mqc.py &

