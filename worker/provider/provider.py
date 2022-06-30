from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from worker.constants import EMAIL_SENDER
from worker.provider.email_service import (AbstractEmailService,
                                           SmtpEmailService)


class AbstractProvide(ABC):

    @abstractmethod
    def send_message(self, *args, **kwargs):
        pass


class EmailProvider(AbstractProvide):

    def __init__(self, email_service: AbstractEmailService = SmtpEmailService):
        self.email_service = email_service

    def send_message(self, *args, **kwargs):
        self._send_email(*args, **kwargs)

    def _send_email(self, template_path: str, template_params: dict,
                    subject: str, email: str):
        email_message = self._get_email(template_path, template_params, subject, email)
        self.email_service.send_email(email=email, email_message=email_message)

    def _get_email(self, template_path: str, template_params: dict,
                   subject: str, email: str):
        email_message = MIMEMultipart('alternative')

        email_message['From'] = EMAIL_SENDER
        email_message['To'] = email
        email_message['Subject'] = subject

        template = self._load_template(template_path, template_params)
        html_template = MIMEText(template, 'html')
        email_message.attach(html_template)
        return email_message

    @staticmethod
    def _load_template(template_path: str, template_params: dict) -> str:
        path = Path(__file__).parent.parent.parent.joinpath('templates')

        template_loader = FileSystemLoader(searchpath=path)
        template_env = Environment(loader=template_loader)
        template = template_env.get_template(template_path)

        return template.render(**template_params)


class SmsProvider(AbstractProvide):

    def send_message(self, *args, **kwargs):
        print("Sending a message to the client through sms")


class MessangerProvider(AbstractProvide):

    def send_message(self, *args, **kwargs):
        print("Sending a message to the client through telegram")
