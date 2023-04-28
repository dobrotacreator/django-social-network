FROM python:3.10-slim-bullseye as base
WORKDIR /app
COPY Pipfile* /app/
RUN pip install pipenv \
    && pipenv install --system
COPY django_social /app/

FROM base as celery
COPY entrypoint_celery.sh /app
RUN chmod +x entrypoint_celery.sh
CMD ["celery", "-A", "django_social", "worker", "-l", "info"]

FROM base as django
COPY entrypoint_django.sh /app
RUN chmod +x entrypoint_django.sh
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
