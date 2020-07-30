#!/usr/bin/bash

rm -rf env
python -m venv env
pip install --upgrade pip -r requirements.txt
