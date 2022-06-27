import psycopg2

from backoff import backoff
from config import PG_DSL


class DBConnector:
    def __init__(self):
        self.db = None
        self.connect()

    @backoff()
    def connect(self) -> None:
        self.connection = psycopg2.connect(**PG_DSL)

    @backoff()
    def select(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    @backoff()
    def create_or_update(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def __del__(self) -> None:
        if self.connection:
            self.connection.close()
