FROM python:3.9-slim-buster

WORKDIR /cron_job
COPY ./cron_job/requirements.txt requirements.txt

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "/wait && python main.py"]