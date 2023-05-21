#!/bin/bash

sleep 10
cd /app/django_social
celery -A django_social worker --loglevel=INFO
