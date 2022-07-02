import logging
import smtplib
import ssl
from abc import ABC, abstractmethod

from worker.constants import EMAIL_PASSWORD, EMAIL_SENDER


class AbstractEmailService(ABC):

    @abstractmethod
    def send_email(self, *args, **kwargs):
        pass


class SmtpEmailService(AbstractEmailService):
    logger = logging.getLogger(__name__)

    @classmethod
    def send_email(cls, *args, **kwargs):
        cls._send_email(*args, **kwargs)

    @classmethod
    def _send_email(cls, email: str, email_message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, email, email_message.as_string())
            cls.logger.info(f"Email sent to: {email}")
