import json
import logging

import pika
from logger import configure_logger
from worker.constants import RABBITMQ_HOST, QUEUE, ProviderType
from utils import is_valid_message, update_history
from worker.provider.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)


def send_notification(ch, method, properties, body):
    message = json.loads(body)
    logger.info(" [x] Received %r" % message)

    try:
        if is_valid_message(message):
            notification_id = message.pop('notification_id')
            is_last = message.pop('is_last')
            provider = ProviderFactory(ProviderType.email).get_provider()
            provider.send_message(**message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(" [x] Done")
        else:
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            logger.error(f"{message} is not valid")
            return

        if is_last:
            update_history(notification_id)
            logger.info(f"Notification with id: {notification_id} is completed")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == '__main__':
    configure_logger()
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE, on_message_callback=send_notification)

    try:
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Consume error: {e}")
        channel.stop_consuming()

    channel.close()
