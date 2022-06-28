from http import HTTPStatus

from fastapi import APIRouter, Depends, Query

from api.v1.params import AdminNotification, CheckEmail
from core.schema import (History, HistoryStatus, MailCheckerMessage,
                         Notification, Task)
from core.settings import CHECK_EMAIL_TEMPLATE_ID
from db.postgres import (get_history_repository, get_notification_repository,
                         get_task_repository, get_template_repository)
from db.queque import get_email_cheker_queue_publisher

router = APIRouter()


@router.post('email/check')
async def check_email(
        payload: CheckEmail,
        history=Depends(get_history_repository),
        notification=Depends(get_notification_repository),
        template=get_template_repository,
        publisher=Depends(get_email_cheker_queue_publisher)
):
    template_object = template.get_by_id(CHECK_EMAIL_TEMPLATE_ID)

    notification_object = Notification(**payload.dict(exclude_none=True))
    notification_object = notification.create(notification_object)

    history_object = History(notification_id=notification_object.notification_id, status=HistoryStatus.CREATED)
    history.create(history_object)

    message = MailCheckerMessage(
        notification_id=notification_object.notification_id,
        template_path=template_object.path,
        template_params=payload.template_params,
        email=payload.email)

    publisher.publish(message.json())
    return {}, HTTPStatus.CREATED


@router.post('/admin/task')
async def create_admin_task(
        payload: AdminNotification,
        history=Depends(get_history_repository),
        notification=Depends(get_notification_repository),
        task=Depends(get_task_repository)
):
    notification_object = Notification(**payload.dict(exclude_none=True))
    notification_object = notification.create(notification_object)

    history_object = History(notification_id=notification_object.notification_id, status=HistoryStatus.CREATED)
    history.create(history_object)

    task_object = Task(execution_time=payload.execution_time, notification_id=notification_object.notification_id)
    task.create(task_object)

    return {}, HTTPStatus.CREATED

