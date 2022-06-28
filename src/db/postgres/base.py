import json

from asyncpg import Record

from core.dependencies import get_repository_pool
from core.schema import ORJSONModel
from db.abstract import AbstractRepository


class BasePostgresRepository(AbstractRepository):
    table: str

    def __init__(self):
        self.pool = get_repository_pool()

    async def create(self, item: ORJSONModel) -> ORJSONModel or None:
        fields = []
        values = []
        for field, value in item.dict(exclude_none=True).items():
            fields.append(field)
            values.append(json.dumps(value) if isinstance(value, dict) else value)
        fields = ', '.join(fields)
        query = f"""
        INSERT INTO {self.table}({fields})
        VALUES({', '.join(f"${val}" for val in range(1, len(values) + 1))})
        RETURNING id, {fields};"""
        return await self.fetch(query, values)

    async def fetch(self, query: str, params: list) -> list[Record]:
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *params, timeout=5)
