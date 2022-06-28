import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from schema import NotificationSchema

load_dotenv()
logger = logging.getLogger(__name__)


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
QUEUE = os.getenv('QUEUE')


def is_valid_message(message: dict) -> bool:
    try:
        NotificationSchema(**message)
        return True
    except Exception:
        return False


def get_email(template_path: str, template_params: dict,
              subject: str, email: str):
    email_message = MIMEMultipart('alternative')

    email_message['From'] = EMAIL_SENDER
    email_message['To'] = email
    email_message['Subject'] = subject

    template = load_template(template_path, template_params)
    html_template = MIMEText(template, 'html')
    email_message.attach(html_template)
    return email_message


def load_template(template_path: str, template_params: dict) -> str:
    path = Path(__file__).parent.parent.joinpath('templates')

    template_loader = FileSystemLoader(searchpath=path)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_path)

    return template.render(**template_params)


def update_history(notification_id: int):
    dsn = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': 5432
    }
    logger.info(dsn)
    connection = psycopg2.connect(**dsn)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO history (created_at, notification_id, status) VALUES(%s, %s, %s)",
                       (datetime.now(), notification_id, 'done'))
        logger.info(f"History is updated for notification_id: {notification_id}")
    except Exception as e:
        logger.error(f"History update error: {e}")
    finally:
        connection.commit()
        cursor.close()
        connection.close()
