# app/auth/service.py
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.auth.models import EmailSchema
from app.core.config import SETTINGS
from pathlib import Path
import random

async def send_email_verifi_code(email: EmailSchema):
    """ 
    email verification code 
    args:
        email: EmailSchema
    """
    conf = ConnectionConfig(
        MAIL_USERNAME = SETTINGS.MAIL_USERNAME,
        MAIL_PASSWORD = SETTINGS.MAIL_PASSWORD,
        MAIL_FROM = SETTINGS.MAIL_FROM,
        MAIL_PORT = SETTINGS.MAIL_PORT,
        MAIL_SERVER = SETTINGS.MAIL_SERVER,
        MAIL_STARTTLS = SETTINGS.MAIL_STARTTLS,
        MAIL_SSL_TLS = SETTINGS.MAIL_SSL_TLS,
        USE_CREDENTIALS = SETTINGS.USE_CREDENTIALS,
        VALIDATE_CERTS = SETTINGS.VALIDATE_CERTS,
        TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
    )
    # random int 6 digits
    code = random.randint(100000, 999999)

    message = MessageSchema(
            subject="Work In Korea Verification Code",
            recipients=email.dict().get("email"),
            template_body={"code": code},
            subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message, template_name="email_code_temp.html")