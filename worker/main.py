import json
import logging
import smtplib
import ssl

import pika
from logger import configure_logger
from utils import (EMAIL_PASSWORD, EMAIL_SENDER, RABBITMQ_HOST, get_email,
                   is_valid_message, update_history, QUEUE)

logger = logging.getLogger(__name__)


def send_email(template_path: str, template_params: dict,
               subject: str, email: str):
    email_message = get_email(template_path, template_params, subject, email)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, email, email_message.as_string())
        logger.info(f"Email sent to: {email}")


def send_notification(ch, method, properties, body):
    message = json.loads(body)
    logger.info(" [x] Received %r" % message)

    try:
        if is_valid_message(message):
            notification_id = message.pop('notification_id')
            is_last = message.pop('is_last')
            # send_email(**message)
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
