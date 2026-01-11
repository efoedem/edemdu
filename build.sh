#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Clean old static files and collect fresh ones
python manage.py collectstatic --no-input --clear
python manage.py migrate