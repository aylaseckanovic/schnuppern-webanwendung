#!/usr/bin/bash

rm -rf env
python3 -m venv env
. env/bin/activate
pip3 install --upgrade pip -r requirements.txt
