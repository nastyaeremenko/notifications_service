import pika

from core.dependencies import get_queue_connection
from core.settings import RABBIT_CHECK_EMAIL_QUEUE_NAME
from db.abstract import AbstractQueuePublisher


class BaseRabbitQueuePublisher(AbstractQueuePublisher):
    queue_name: str

    def __init__(self):
        self.connection = get_queue_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=RABBIT_CHECK_EMAIL_QUEUE_NAME, durable=True)

    def publish(self, message: str) -> None:
        self.channel.basic_publish(
            exchange='',
            routing_key=RABBIT_CHECK_EMAIL_QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
