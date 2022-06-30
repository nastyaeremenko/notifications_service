FROM python:3.9-slim-buster

WORKDIR /usr/src/worker

RUN pip install --upgrade pip
COPY ./worker/requirements.txt requirements.txt

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN pip install -r requirements.txt

COPY . .
COPY ../templates ../templates

CMD ["sh", "-c", "/wait && python main.py"]
