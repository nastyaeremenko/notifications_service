import json
import sys
import logging
import smtplib
import ssl

import pika

from logger import configure_logger
from utils import (is_valid_message, update_history, get_email,
                   RABBITMQ_HOST, EMAIL_PASSWORD, EMAIL_SENDER)


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
    if is_valid_message(message):
        notification_id = message.pop('notification_id')
        logger.info(" [x] Received %r" % message)
        send_email(**message)
    else:
        logger.error(f"{message} is not valid")
    logger.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # update_history(notification_id)


if __name__ == '__main__':
    configure_logger()
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    queue = sys.argv[1]

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=send_notification)

    try:
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Consume error: {e}")
        channel.stop_consuming()

    connection.close()
