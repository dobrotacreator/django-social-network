#!/bin/bash

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000