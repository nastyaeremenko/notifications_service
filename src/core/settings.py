import os

PROJECT_NAME = os.getenv('PROJECT_NAME', 'Notification')
DEBUG = os.getenv('DEBUG', True)

POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME', 'notification')
POSTGRES_DB_USER = os.getenv('POSTGRES_DB_USER', 'postgres')
POSTGRES_DB_PASSWORD = os.getenv('POSTGRES_DB_PASSWORD', '11111111')
POSTGRES_DB_HOST = os.getenv('POSTGRES_DB_HOST', 'localhost')
POSTGRES_DB_PORT = os.getenv('POSTGRES_DB_PORT', 5432)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
