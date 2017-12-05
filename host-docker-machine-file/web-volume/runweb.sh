#!/bin/bash

cd /src/avocado_project

python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

gunicorn avocado_project.wsgi -b 0.0.0.0:8000