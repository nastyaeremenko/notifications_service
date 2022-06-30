import psycopg2

from backoff import backoff
from config import PG_DSL


class DBConnector:
    def __init__(self):
        self.connection = None
        self.connect()

    @backoff()
    def connect(self) -> None:
        self.connection = psycopg2.connect(**PG_DSL)

    @backoff()
    def select(self, query, params):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        cursor.close()
        columns_names = [column[0] for column in cursor.description]
        result = []
        for record in records:
            result.append(dict(zip(columns_names, record)))
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
