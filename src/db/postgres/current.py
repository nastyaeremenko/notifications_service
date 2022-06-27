from core.schema import Template
from db.postgres.base import BasePostgresRepository


class NotificationRepository(BasePostgresRepository):
    table = 'notification'


class HistoryRepository(BasePostgresRepository):
    table = 'history'


class TaskRepository(BasePostgresRepository):
    table = 'task'


class TemplateRepository(BasePostgresRepository):
    table = 'template'

    async def get_by_id(self, template_id) -> Template:
        query = f"""SELECT path, params FROM template WHERE id = '{template_id}';"""
        data = self.fetch(query, [])[0]
        return Template(**data)
