import os
from logging import config as logging_config

from dotenv import load_dotenv

from cron_job.logger import LOG_CONFIG

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOG_CONFIG)

# Настройки Postgres
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PG_DSL = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}
