import json
import logging
from abc import abstractmethod
from datetime import datetime
from logging import config as logging_config

import pika
from apscheduler.schedulers.blocking import BlockingScheduler

import queries
from api_utils import (get_user_data, get_popular_movies,
                       get_movies_data)
from config import LOG_CONFIG
from db_utils import DBConnector

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
        self.channel.queue_declare(queue=self.queue_name,
                                   durable=True)
        for message in self._get_data(users_dict):
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(' [x] Sent %r' % message)

    def run(self):
        scheduler = self.scheduler
        scheduler.add_job(self.send, self.periodicity_type,
                          **self.periodicity_param)
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit) as e:
            logging.error(e)


class AdminCronJob(CronJob):
    def _get_data(self, users_dict: dict):
        users_data = get_user_data()
        template_path = self.db_conn.select(queries.get_template_path, [self.template_id])
        count_messages = len(users_data)
        for i, user_data in enumerate(users_data):
            yield {
                'notification_id': users_dict['notification_id'],
                'template_path': template_path,
                'template_params': {
                    'title': users_dict['title'],
                    'body': users_dict['body'],
                    'username': users_data['username']
                },
                'subject': users_dict['subject'],
                'email': user_data['email'],
                'is_last': count_messages == i
            }

    def _db_interaction(self, task_id=None):
        if not task_id:
            logging.error('Отсутствует task_id в AdminCronJob.')
        notification_id = self.db_conn.select(queries.get_notification_id_in_task, [task_id])
        self.db_conn.create_or_update(queries.create_history, [notification_id, 'in_progress'])
        self.db_conn.create_or_update(queries.change_task_status, ['in_progress', notification_id])
        return self.db_conn.select(queries.get_notification_data, [notification_id])[0]

    def send(self, notification_id=None):
        current_time = datetime.now()
        tasks = self.db_conn.select(queries.check_task, [current_time])
        if not tasks:
            return
        for task in tasks:
            super().send(task['id'])


class SchedulerCronJob(CronJob):
    def _get_data(self, users_dict: dict):
        users_data = get_user_data()
        movies = get_popular_movies()
        movies_data = get_movies_data(movies)
        template_path = self.db_conn.select(queries.get_template_path, [self.template_id])
        count_messages = len(users_data)
        for i, user_data in enumerate(users_data):
            yield {
                'notification_id': users_dict['notification_id'],
                'template_path': template_path,
                'template_params': {
                    'username': users_data['username'],
                    'movies': movies_data
                },
                'subject': 'Пятничная подборка фильмов',
                'email': user_data['email'],
                'is_last': count_messages == i
            }

    def _db_interaction(self, task_id=None):
        notification_id = self.db_conn.create_or_update(queries.create_notification, [self.template_id])
        self.db_conn.create_or_update(queries.create_history, [notification_id, 'in_progress'])
        return self.db_conn.select(queries.get_notification_data, [notification_id])[0]


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    db_connection = DBConnector()

    AdminCronJob({'minute': 1}, 'interval', channel, 'admin_cron', 1, DBConnector)
    SchedulerCronJob({'day_of_week': 'fri'}, 'cron', channel, 'friday_cron', 2, DBConnector)

    connection.close()
