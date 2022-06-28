FROM python:3.9-slim-buster

WORKDIR /cron_job
COPY ./cron_job/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./cron_job .