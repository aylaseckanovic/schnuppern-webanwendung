#!/usr/bin/bash

rm -rf env
python -m venv env
. env/bin/activate
pip install --upgrade pip -r requirements.txt
