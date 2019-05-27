#!/bin/bash
chmod +x venv-linux/bin/*&&
source venv-linux/bin/activate&&
nohup venv-linux/bin/python -u mqc.py &

