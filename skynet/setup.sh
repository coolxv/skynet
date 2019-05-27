#!/bin/bash

rm -rf venv;
rm -rf migrations;
rm -rf data/*;
pip install --upgrade setuptools > /dev/null 2>&1;
pip install --upgrade pip > /dev/null 2>&1;
pip install --upgrade virtualenv > /dev/null 2>&1;
virtualenv venv&&
source venv/bin/activate&&
export FLASK_CONFIG=production&&
venv/bin/pip install --upgrade setuptools > /dev/null 2>&1;
venv/bin/pip install --upgrade pip > /dev/null 2>&1;
venv/bin/pip install -r requirements.txt&&
venv/bin/python manage.py db init&&
venv/bin/python manage.py db migrate&&
venv/bin/python manage.py db upgrade&&
nohup venv/bin/python manage.py runserver -d -r -h 0.0.0.0 -p 5558& > /dev/null 2>&1