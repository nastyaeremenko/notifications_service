from dataclasses import dataclass


@dataclass
class NotificationSchema:
    notification_id: int
    template_path: str
    template_params: dict
    subject: str
    email: str
    is_last: bool
