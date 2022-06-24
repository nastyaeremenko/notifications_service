import os
import logging
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import psycopg2
from jinja2 import FileSystemLoader, Environment
from dotenv import load_dotenv

from schema import NotificationSchema


load_dotenv()
logger = logging.getLogger(__name__)


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


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
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': 5432
    }
    connection = psycopg2.connect(**dsn)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO history (notification_id, status) VALUES(%s, %s)",
                       (notification_id, 'done'))
    except Exception as e:
        logger.error(f"History update error: {e}")
    finally:
        connection.commit()
        cursor.close()
        connection.close()
