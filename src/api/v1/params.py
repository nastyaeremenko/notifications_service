from datetime import datetime

from pydantic import EmailStr, Field

from core.schema import ORJSONModel


class CheckEmail(ORJSONModel):
    email: EmailStr = Field(..., description='Email адресс пользователя для проверки.')
    template_params: dict = Field(..., description='Параметры шаблона')


class AdminNotification(ORJSONModel):
    execution_time: datetime = Field(default_factory=datetime.now)
    template_id: int = Field(..., description='ID используемого шаблона.')
    template_params: dict = Field(..., description='Параметры для вставки в шаблон.')
    role: str = Field(None, description='Роль пользователей для отправки email.')
    permission: str = Field(None, description='Уровень прав пользователей для отправки email.')
    email: str = Field(None, description='email пользователя для отправки email.')
