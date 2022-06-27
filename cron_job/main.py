import json
from abc import abstractmethod

import pika
from apscheduler.schedulers.blocking import BlockingScheduler

from db_utils import (create_notification, create_history,
                      check_task, change_task_status, 
                      get_users_dict, get_template_path,
                      get_notification_id_in_task)
from api_utils import (get_user_data, get_popular_movies,
                       get_movies_data)


class CronJob:
    def __init__(self, periodicity_param, periodicity_type,
                 channel, queue_name, template_id):
        self.periodicity_param = periodicity_param
        self.periodicity_type = periodicity_type
        self.channel = channel
        self.queue_name = queue_name
        self.scheduler = BlockingScheduler()
        self.template_id = template_id

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
        except (KeyboardInterrupt, SystemExit):
            pass


class AdminCronJob(CronJob):
    def _get_data(self, users_dict: dict):
        users_data = get_user_data()
        template_path = get_template_path(self.template_id)
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
            pass
        notification_id = get_notification_id_in_task(task_id)
        create_history(notification_id)
        change_task_status(notification_id)
        return get_users_dict(notification_id, task_id)

    def send(self, notification_id=None):
        tasks = check_task()
        if not tasks:
            return
        for task in tasks:
            super().send(task['id'])


class SchedulerCronJob(CronJob):
    def _get_data(self, users_dict: dict):
        users_data = get_user_data()
        movies = get_popular_movies()
        movies_data = get_movies_data(movies)
        template_path = get_template_path(self.template_id)
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
        notification_id, users_dict = create_notification()
        create_history(notification_id)
        return users_dict


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    AdminCronJob({'minute': 1}, 'interval', channel, 'admin_cron', 1)
    SchedulerCronJob({'day_of_week': 'fri'}, 'cron', channel, 'friday_cron', 2)

    connection.close()
