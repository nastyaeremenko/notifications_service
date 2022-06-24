import json
import sys
import os
import logging

import pika
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail

from logger import configure_logger
from utils import is_valid_message, update_history, load_template, RABBITMQ_HOST


logger = logging.getLogger(__name__)
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))


def send_email(template_path: str, template_params: dict,
               subject: str, email: str):
    from_email = Email("test@example.com")
    to_email = To(email)
    template = load_template(template_path, template_params)
    content = Content(mime_type="text/html", content=template)
    mail = Mail(from_email, to_email, subject, content)
    # response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)


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
