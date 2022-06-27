import pika
from fastapi import Depends

from core.settings import RABBIT_CHECK_EMAIL_QUEUE_NAME
from core.dependencies import get_queque_connection
from db.abstract import AbstractQueuePublisher


class BaseRabbitQueuePublisher(AbstractQueuePublisher):
    queue_name: str

    def __init__(self, connection: pika.BlockingConnection = Depends(get_queque_connection)):
        self.connection = connection
        self.channel = connection.channel()
        self.chanel.queue_declare(queue=RABBIT_CHECK_EMAIL_QUEUE_NAME, durable=True)

    async def publish(self, message: str) -> None:
        self.channel.basic_publish(
            exchange='',
            routing_key=RABBIT_CHECK_EMAIL_QUEUE_NAME,
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
