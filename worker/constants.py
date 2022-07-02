import os
from enum import Enum, auto

from dotenv import load_dotenv

load_dotenv()


class ProviderType(Enum):
    email = auto()
    sms = auto()
    messanger = auto()


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
QUEUE = os.getenv('QUEUE')
