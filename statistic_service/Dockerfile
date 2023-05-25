FROM python:3.10-slim-bullseye
WORKDIR /webapp
COPY . .
RUN pip install pipenv \
    && pipenv install --system

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
