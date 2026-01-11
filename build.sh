#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate

# Add this line to import your courses
if [ -f data.json ]; then
    python manage.py loaddata data.json
fi

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi