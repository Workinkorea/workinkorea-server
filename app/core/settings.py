# app/core/settings.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # URL 설정
    COOKIE_DOMAIN: Optional[str] = None
    CLIENT_URL: Optional[str] = None
    ORIGINS_URLS: Optional[str] = None

    # 이메일 설정
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM_NAME: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None

    # 데이터베이스 설정
    DATABASE_SYNC_URL: Optional[str] = None
    DATABASE_ASYNC_URL: Optional[str] = None

    # redis 설정
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None
    REDIS_DB: Optional[int] = None

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


    # 어드민 전용 jwt 설정 -> 메일주소랑 같이 확인해야함.
    ADMIN_JWT_SECRET: Optional[str] = None
    ADMIN_JWT_ALGORITHM: Optional[str] = None
    ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None
    ADMIN_REFRESH_TOKEN_EXPIRE_MINUTES: Optional[int] = None

    # admin 설정 -> 어드민 메일주소는 콤마로 구분됨.
    # 예를들어서 -> .env에 ADMIN_EMAILS=admin1@example.com,admin2@example.com,admin3@example.com 이런식으로 입력해야함.
    ADMIN_EMAILS: Optional[str] = None

    # minio 설정
    MINIO_ENDPOINT: Optional[str] = None
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    MINIO_BUCKET_NAME: Optional[str] = None
    
    class Config:
        env_file = ".env"


SETTINGS = Settings()
