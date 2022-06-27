from db.postgres.current import NotificationRepository, HistoryRepository, TaskRepository, TemplateRepository
from db.queque.current import EmailCheckerPublisher

pool = None
queque = None


def get_repository_pool():
    return pool


def get_queque_connection():
    return queque


def get_notification_repository() -> NotificationRepository:
    return NotificationRepository()


def get_history_repository() -> HistoryRepository:
    return HistoryRepository()


def get_task_repository() -> TaskRepository:
    return TaskRepository()


def get_template_repository() -> TemplateRepository:
    return TemplateRepository()


def get_email_cheker_queue_publisher() -> EmailCheckerPublisher:
    return EmailCheckerPublisher()
