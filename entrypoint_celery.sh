#!/bin/bash

sleep 10
cd /app
celery -A django_social worker --loglevel=INFO
