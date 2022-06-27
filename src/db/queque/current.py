from core.settings import CHECK_EMAIL_TEMPLATE_NAME
from db.queque.base import BaseRabbitQueuePublisher


class EmailCheckerPublisher(BaseRabbitQueuePublisher):
    queue_name = CHECK_EMAIL_TEMPLATE_NAME
