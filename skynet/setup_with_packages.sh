#!/bin/bash
rm -rf migrations;
rm -rf data/*;
chmod +x venv-linux/bin/*&&
source venv-linux/bin/activate&&
export FLASK_CONFIG=production&&
venv-linux/bin/python manage.py db init&&
venv-linux/bin/python manage.py db migrate&&
venv-linux/bin/python manage.py db upgrade&&
nohup venv-linux/bin/python manage.py runserver -d -r -h 0.0.0.0 -p 5558& > /dev/null 2>&1

