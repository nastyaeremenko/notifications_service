from pydantic import Field, EmailStr
from datetime import datetime
from core.schema import ORJSONModel


class CheckEmail(ORJSONModel):
    email: EmailStr = Field(..., description='Email адресс пользователя для проверки.')
    username: str = Field(..., description='Пользовательский логин.')


class AdminNotification(ORJSONModel):
    execution_time: datetime = Field(default_factory=datetime.now)
    template_id: int = Field(..., description='ID используемого шаблона.')
    params: dict = Field(..., description='Параметры для вставки в шаблон.')
    role: str = Field(None, description='Роль пользователей для отправки email.')
    permission: str = Field(None, description='Уровень прав пользователей для отправки email.')
    email: str = Field(None, description='email пользователя для отправки email.')
