from abc import ABC, abstractmethod
import smtplib
import ssl
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from worker.constants import EMAIL_PASSWORD, EMAIL_SENDER


class AbstractProvide(ABC):

    @abstractmethod
    def send_message(self, *args, **kwargs):
        pass


class EmailProvider(AbstractProvide):
    logger = logging.getLogger(__name__)

    def send_message(self, *args, **kwargs):
        self._send_email(*args, **kwargs)

    def _send_email(self, template_path: str, template_params: dict,
                    subject: str, email: str):
        email_message = self._get_email(template_path, template_params, subject, email)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, email, email_message.as_string())
            self.logger.info(f"Email sent to: {email}")

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
        path = Path(__file__).parent.parent.joinpath('templates')

        template_loader = FileSystemLoader(searchpath=path)
        template_env = Environment(loader=template_loader)
        template = template_env.get_template(template_path)

        return template.render(**template_params)


class SmsProvider(AbstractProvide):

    def send_message(self, *args, **kwargs):
        print("Sending message to client through sms")


class MessangerProvider(AbstractProvide):

    def send_message(self, *args, **kwargs):
        print("Sending message to client through telegram")
