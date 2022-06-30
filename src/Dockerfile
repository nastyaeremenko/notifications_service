FROM python:3.9-slim-buster

WORKDIR /src/app
COPY ./src/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src/ .

RUN python manage.py migrate
CMD  ['/bin/sh','-c', 'python manage.py run_server']
