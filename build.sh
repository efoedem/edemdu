#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Clean old static files and collect fresh ones
python manage.py collectstatic --no-input --clear

# Apply migrations to the new PostgreSQL database
python manage.py migrate

# Create a superuser if variables are provided (Essential for Free Tier)
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi