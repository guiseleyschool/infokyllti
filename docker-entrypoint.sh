#!/bin/sh
pipenv run python3 ./manage.py migrate
exec multirun "pipenv run gunicorn -c python:infokyllti.gunicorn infokyllti.wsgi"