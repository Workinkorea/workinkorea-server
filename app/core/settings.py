# app/core/settings.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # URL 설정
    COOKIE_DOMAIN: Optional[str] = None
    CLIENT_URL: Optional[str] = None

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

    # 데이터베이스 설정
    DATABASE_SYNC_URL: Optional[str] = None
    DATABASE_ASYNC_URL: Optional[str] = None

    # google login 설정
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None
    GOOGLE_AUTHORIZATION_URL: Optional[str] = None
    GOOGLE_TOKEN_URL: Optional[str] = None
    GOOGLE_USER_INFO_URL: Optional[str] = None

    # jwt 설정
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None
    REFRESH_TOKEN_EXPIRE_MINUTES: Optional[int] = None

    class Config:
        env_file = ".env"


SETTINGS = Settings()
