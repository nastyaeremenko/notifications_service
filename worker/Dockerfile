FROM python:3.9-slim-buster

WORKDIR /usr/src/worker

RUN pip install --upgrade pip
COPY ./worker/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY ../templates ../templates

CMD ["python", "main.py"]
