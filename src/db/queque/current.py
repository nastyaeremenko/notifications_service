from db.queque.base import BaseRabbitQueuePublisher
from core.settings import CHECK_EMAIL_TEMPLATE_NAME


class EmailCheckerPublisher(BaseRabbitQueuePublisher):
    queue_name = CHECK_EMAIL_TEMPLATE_NAME
