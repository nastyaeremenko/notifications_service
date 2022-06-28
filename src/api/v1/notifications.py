from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.v1.params import AdminNotification, CheckEmail
from core.schema import (History, HistoryStatus, MailCheckerMessage,
                         Notification, Task, TaskStatus)
from core.settings import CHECK_EMAIL_TEMPLATE_ID, CHECK_EMAIL_TEMPLATE_SUBJECT
from db.postgres import (get_history_repository, get_notification_repository,
                         get_task_repository, get_template_repository)
from db.queque import get_email_cheker_queue_publisher

router = APIRouter()


@router.post('/email/check')
async def check_email(
        payload: CheckEmail,
        history=Depends(get_history_repository),
        notification=Depends(get_notification_repository),
        template=Depends(get_template_repository),
        publisher=Depends(get_email_cheker_queue_publisher)
):
    template_object = await template.get_by_id(CHECK_EMAIL_TEMPLATE_ID)

    notification_object = Notification(**payload.dict(exclude_none=True))
    notification_object = await notification.create(notification_object)

    history_object = History(notification_id=notification_object[0]['id'],
                             status=HistoryStatus.CREATED)
    await history.create(history_object)

    message = MailCheckerMessage(
        notification_id=notification_object[0]['id'],
        template_path=template_object.path,
        template_params=payload.template_params,
        email=payload.email,
        subject=CHECK_EMAIL_TEMPLATE_SUBJECT,
        is_last=True)

    publisher.publish(message.json())
    return JSONResponse(content={'message': 'Message is published'},
                        status_code=HTTPStatus.CREATED)


@router.post('/admin/task')
async def create_admin_task(
        payload: AdminNotification,
        history=Depends(get_history_repository),
        notification=Depends(get_notification_repository),
        task=Depends(get_task_repository)
):
    notification_object = Notification(**payload.dict(exclude_none=True))
    notification_object = await notification.create(notification_object)

    history_object = History(notification_id=notification_object[0]['id'],
                             status=HistoryStatus.CREATED)
    await history.create(history_object)

    task_object = Task(execution_time=payload.execution_time,
                       notification_id=notification_object[0]['id'],
                       status=TaskStatus.CREATED)
    await task.create(task_object)

    return JSONResponse(content={'message': 'Task is crated'},
                        status_code=HTTPStatus.CREATED)
