#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,  sys
if sys.platform == 'win32':
    cmd = 'rd /s/q venv&' \
          'rd /s/q migrations&' \
          'del /f/s/q data\\*&' \
          'pip install --upgrade setuptools >nul&' \
          'pip install --upgrade pip >nul&' \
          'pip install --upgrade virtualenv >nul&' \
          'virtualenv venv&&' \
          'venv\\Scripts\\activate.bat&&' \
          'set FLASK_CONFIG=production&&' \
          'venv\\Scripts\\pip install --upgrade setuptools >nul&' \
          'venv\\Scripts\\pip install --upgrade pip >nul&' \
          'venv\\Scripts\\pip install -r requirements.txt&&' \
          'venv\\Scripts\\python manage.py db init&&' \
          'venv\\Scripts\\python manage.py db migrate&&' \
          'venv\\Scripts\\python manage.py db upgrade&&' \
          'venv\\Scripts\\python manage.py runserver -d -r -h 0.0.0.0 -p 5558'
    os.system(cmd)
else:
    cmd = 'rm -rf venv;' \
          'rm -rf migrations;' \
          'rm -rf data/*;' \
          'pip install --upgrade setuptools > /dev/null 2>&1;' \
          'pip install --upgrade pip > /dev/null 2>&1;' \
          'pip install --upgrade virtualenv > /dev/null 2>&1;' \
          'virtualenv venv&&' \
          'source venv/bin/activate&&' \
          'export FLASK_CONFIG=production&&' \
          'venv/bin/pip install --upgrade setuptools > /dev/null 2>&1;' \
          'venv/bin/pip install --upgrade pip > /dev/null 2>&1;' \
          'venv/bin/pip install -r requirements.txt&&' \
          'venv/bin/python manage.py db init&&' \
          'venv/bin/python manage.py db migrate&&' \
          'venv/bin/python manage.py db upgrade&&' \
          'nohup venv/bin/python manage.py runserver -d -r -h 0.0.0.0 -p 5558& > /dev/null 2>&1'
    os.system(cmd)




