from datetime import datetime
from enum import Enum

import orjson
from pydantic import BaseModel, Field

from core.settings import CHECK_EMAIL_TEMPLATE_ID


class HistoryStatus(Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'Done'


class TaskStatus(Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    CANCELED = 'canceled'
    PROCESS_ERROR = 'process_error'


class NotificationType(Enum):
    SMS = 'sms'
    EMAIL = 'email'
    TELEGRAM = 'telegram'


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True


class Notification(ORJSONModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    template_id: int = Field(
        CHECK_EMAIL_TEMPLATE_ID, description='ID шаблона по которому осуществляется отправка email.'
    )
    template_params: dict = Field(..., description='Параметры для вставки в шаблон.')
    role: str = Field(None, description='Роль пользователей для отправки email.')
    permission: str = Field(None, description='Уровень прав пользователей для отправки email.')
    email: str = Field(None, description='Email пользователя для отправки email.')
    notification_type: NotificationType = Field(NotificationType.EMAIL, description='Тип оповещения')


class History(ORJSONModel):
    created_at: datetime = Field(default_factory=datetime.now)
    notification_id: int = Field(..., description='ID уведомления.')
    status: HistoryStatus = Field(..., description='Статус выполнения отправки уведомления.')


class Task(ORJSONModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    execution_time: datetime = Field(default_factory=datetime.now)
    notification_id: int = Field(..., description='ID уведомления.')
    status: TaskStatus = Field(..., description='Статус выполнения задачи.')


class Template(ORJSONModel):
    path: str = Field(..., description='Адрес шаблона.')


class MailCheckerMessage(ORJSONModel):
    notification_id: int = Field(None, description='ID уведомления.')
    template_path: str = Field(..., description='Адрес шаблона.')
    template_params: dict = Field(..., description='Параметры шаблона.')
    email: str = Field(None, description='Email пользователя для отправки email.')
    subject: str = Field(..., description='Subject для имейла')
    is_last: bool = Field(..., description='Идентификатор если последний имейл')
