FROM python:3.10-slim-bullseye as base
WORKDIR /app
COPY Pipfile* /app/
RUN pip install pipenv \
    && pipenv install --system
COPY django_social /app/django_social

FROM base as celery
COPY entrypoint_celery.sh /app
RUN chmod +x entrypoint_celery.sh
CMD ["celery", "-A", "django_social.django_social", "worker", "-l", "info"]

FROM base as django
COPY entrypoint_django.sh /app
RUN chmod +x entrypoint_django.sh
WORKDIR /app/django_social
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
