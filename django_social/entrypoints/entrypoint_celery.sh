#!/bin/bash

sleep 10
celery -A django_social worker --loglevel=INFO
