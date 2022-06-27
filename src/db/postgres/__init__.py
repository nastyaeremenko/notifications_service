from db.postgres.current import (HistoryRepository, NotificationRepository,
                                 TaskRepository, TemplateRepository)


def get_notification_repository() -> NotificationRepository:
    return NotificationRepository()


def get_history_repository() -> HistoryRepository:
    return HistoryRepository()


def get_task_repository() -> TaskRepository:
    return TaskRepository()


def get_template_repository() -> TemplateRepository:
    return TemplateRepository()

