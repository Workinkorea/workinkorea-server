# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):

    # 이메일 설정
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None
    MAIL_STARTTLS: Optional[bool] = False
    MAIL_SSL_TLS: Optional[bool] = True
    USE_CREDENTIALS: Optional[bool] = True
    VALIDATE_CERTS: Optional[bool] = True

    class Config:
        env_file = ".env"

SETTINGS = Settings()
