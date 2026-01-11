#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate



if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi