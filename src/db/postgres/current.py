from core.schema import Notification, History, Task
from db.postgres.base import BasePostgresRepository


class NotificationRepository(BasePostgresRepository):
    table = 'notification'


class HistoryRepository(BasePostgresRepository):
    table = 'history'


class TaskRepository(BasePostgresRepository):
    table = 'task'
