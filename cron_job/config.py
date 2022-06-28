import os

from dotenv import load_dotenv

load_dotenv()

# Настройки Postgres
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))

PG_DSL = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
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
