#!/usr/bin/env bash

source env/bin/activate
FLASK_APP=app.py FLASK_ENV=development flask run
