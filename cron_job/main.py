import json
import logging
from abc import abstractmethod
from datetime import datetime
from logging import config as logging_config

import pika
from apscheduler.schedulers.blocking import BlockingScheduler

import queries
from api_utils import APIRequest
from config import (
    API_ANALYTICS_HOST,
    API_AUTH_HOST,
    API_MOVIES_HOST,
    HEADERS,
    PATH_ANALYTICS_DATA,
    PATH_MOVIES_DATA,
    PATH_USER_DATA,
    RABBITMQ_HOST
)
from db_utils import DBConnector
from logger import LOG_CONFIG

logging_config.dictConfig(LOG_CONFIG)


class CronJob:
    def __init__(self, periodicity_param, periodicity_type,
                 channel, queue_name, template_id, db_conn):
        self.periodicity_param = periodicity_param
        self.periodicity_type = periodicity_type
        self.channel = channel
        self.queue_name = queue_name
        self.scheduler = BlockingScheduler()
        self.template_id = template_id
        self.db_conn = db_conn

    @abstractmethod
    def _get_data(self, users_dict: dict):
        return {}

    @abstractmethod
    def _db_interaction(self, task_id=None):
        pass

    def send(self, task_id=None):
        users_dict = self._db_interaction(task_id)
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        for message in self._get_data(users_dict):
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )

    def run(self):
        scheduler = self.scheduler
        scheduler.add_job(self.send,
                          self.periodicity_type,
                          **self.periodicity_param)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit) as e:
            logging.error(e)


class AdminCronJob(CronJob):
    def _get_data(self, users_dict: dict):
        params = {}
        if 'role' in users_dict and users_dict['role']:
            params['role'] = users_dict['role']
        if 'permission' in users_dict and users_dict['permission']:
            params['permission'] = users_dict['permission']
        if 'email' in users_dict and users_dict['email']:
            params['email'] = users_dict['email']
        users_data = APIRequest(API_AUTH_HOST, PATH_USER_DATA).request(
            method='get', params=params, headers=HEADERS
        )
        template_path = self.db_conn.select(
            queries.get_template_path, [self.template_id]
        )
        count_messages = len(users_data)
        for i, user_data in enumerate(users_data):
            yield {
                'notification_id': users_dict['notification_id'],
                'template_path': template_path,
                'template_params': {
                    'title': users_dict['title'],
                    'body': users_dict['body'],
                    'username': users_data['username'],
                },
                'subject': users_dict['subject'],
                'email': user_data['email'],
                'is_last': count_messages == i,
            }

    def _db_interaction(self, task_id=None):
        if not task_id:
            logging.error('Отсутствует task_id в AdminCronJob.')
        notification_id = self.db_conn.select(
            queries.get_notification_id_in_task, [task_id]
        )
        self.db_conn.create_or_update(
            queries.create_history, [notification_id, 'in_progress']
        )
        self.db_conn.create_or_update(
            queries.change_task_status, ['in_progress', notification_id]
        )
        return self.db_conn.select(queries.get_notification_data,
                                   [notification_id])[0]

    def send(self, notification_id=None):
        current_time = datetime.now()
        tasks = self.db_conn.select(queries.check_task, [current_time])
        if not tasks:
            return
        for task in tasks:
            super().send(task['id'])


class SchedulerCronJob(CronJob):
    def _get_data(self, users_dict: dict):
        params = {}
        if 'role' in users_dict and users_dict['role']:
            params['role'] = users_dict['role']
        if 'permission' in users_dict and users_dict['permission']:
            params['permission'] = users_dict['permission']
        if 'email' in users_dict and users_dict['email']:
            params['email'] = users_dict['email']
        users_data = APIRequest(API_AUTH_HOST, PATH_USER_DATA).request(
            method='get', params=params, headers=HEADERS
        )
        movies = APIRequest(API_ANALYTICS_HOST, PATH_ANALYTICS_DATA).request(
            method='get', headers=HEADERS
        )
        movies_id = [movie['movie_id'] for movie in movies if 'movie_id' in movies]
        movies_data = APIRequest(API_MOVIES_HOST, PATH_MOVIES_DATA).request(
            method='post', data={'movies_id': movies_id}, headers=HEADERS
        )
        template_path = self.db_conn.select(
            queries.get_template_path, [self.template_id]
        )
        count_messages = len(users_data)
        for i, user_data in enumerate(users_data):
            yield {
                'notification_id': users_dict['notification_id'],
                'template_path': template_path,
                'template_params': {
                    'username': users_data['username'],
                    'movies': movies_data,
                },
                'subject': 'Пятничная подборка фильмов',
                'email': user_data['email'],
                'is_last': count_messages == i,
            }

    def _db_interaction(self, task_id=None):
        notification_id = self.db_conn.create_or_update(
            queries.create_notification, [self.template_id]
        )
        self.db_conn.create_or_update(
            queries.create_history, [notification_id, 'in_progress']
        )
        return self.db_conn.select(queries.get_notification_data,
                                   [notification_id])[0]


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    db_connection = DBConnector()

    AdminCronJob(
        {'minute': 1}, 'interval', channel, 'admin_cron', 1, DBConnector
    )
    SchedulerCronJob(
        {'day_of_week': 'fri'}, 'cron', channel, 'friday_cron', 2, DBConnector
    )
    print("Закрывает соединение")
    connection.close()
