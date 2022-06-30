import logging
import os
from datetime import datetime

import psycopg2
from schema import NotificationSchema

logger = logging.getLogger(__name__)


def is_valid_message(message: dict) -> bool:
    try:
        NotificationSchema(**message)
        return True
    except Exception:
        return False


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
