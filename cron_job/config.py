import os

from dotenv import load_dotenv

load_dotenv()

# Настройки Postgres
POSTGRES_NAME = os.getenv('POSTGRES_DB', 'notification')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))

PG_DSL = {
    'dbname': POSTGRES_NAME,
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD,
    'host': POSTGRES_HOST,
    'port': POSTGRES_PORT
}

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Внешние API
SITE_TOKEN = os.getenv('SITE_TOKEN')
HEADERS = {'Authorization': f'Bearer {SITE_TOKEN}'}
API_AUTH_HOST = os.getenv('API_AUTH_HOST')
PATH_USER_DATA = os.getenv('PATH_USER_DATA')
API_ANALYTICS_HOST = os.getenv('API_ANALYTICS_HOST')
PATH_ANALYTICS_DATA = os.getenv('PATH_ANALYTICS_DATA')
API_MOVIES_HOST = os.getenv('API_MOVIES_HOST')
PATH_MOVIES_DATA = os.getenv('PATH_MOVIES_DATA')

# RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
ADMIN_QUEUE = os.getenv('ADMIN_QUEUE', 'admin_cron')
ADMIN_TEMPLATE_ID = int(os.getenv('ADMIN_TEMPLATE_ID', 1))
MOVIES_TOP_QUEUE = os.getenv('MOVIES_TOP_QUEUE', 'friday_cron')
MOVIES_TOP_TEMPLATE_ID = int(os.getenv('MOVIES_TOP_TEMPLATE_ID', 2))
