#!/usr/bin/env bash

set -o errexit  # stop script if error occurs

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate