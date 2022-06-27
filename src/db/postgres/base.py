from asyncpg import Pool, Record
from fastapi import Depends

from core.schema import ORJSONModel
from core.dependencies import get_repository_pool
from db.abstract import AbstractRepository


class BasePostgresRepository(AbstractRepository):
    table: str

    def __init__(self, pool: Pool = Depends(get_repository_pool)):
        self.pool = pool

    async def create(self, item: ORJSONModel) -> ORJSONModel or None:
        fields = []
        values = []
        [(fields.append(str(f)), values.append(str(v))) for f, v in item.dict(exclude_none=True).items()]
        for field, value in item.dict(exclude_none=True).items():
            fields.append(field)
            values.append(str(value)) if not isinstance(value, str) else values.append(f"'{value}'")
        fields = ', '.join(fields)
        query = f"""
        INSERT INTO {self.table}({fields})
        VALUES({', '.join(str(val) for val in range(1, len(values) + 1))})
        RETURNING id, {fields};"""
        await self.fetch(query, values)

    async def fetch(self, query: str, params: list) -> list[Record]:
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *params, timeout=5)



