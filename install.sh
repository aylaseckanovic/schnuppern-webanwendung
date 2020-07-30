#!/usr/bin/bash

rm -rf env
python -m venv env
pip install --upgrade pip -r requirements.txt

rm -f grades.db
sqlite grades.db <tables.sql
