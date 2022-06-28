FROM python:3.9-slim-buster

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY .src/ .

RUN python manage.py migrate
CMD  ['/bin/sh','-c', 'python manage.py run_server']
