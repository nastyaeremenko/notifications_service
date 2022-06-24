import os
import logging
from pathlib import Path

import psycopg2
from jinja2 import FileSystemLoader, Environment
from dotenv import load_dotenv

from schema import NotificationSchema


load_dotenv()
logger = logging.getLogger(__name__)


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')


def is_valid_message(message: dict) -> bool:
    try:
        NotificationSchema(**message)
        return True
    except Exception:
        return False


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
