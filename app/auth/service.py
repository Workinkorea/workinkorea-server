# app/auth/service.py
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.settings import SETTINGS
from app.auth.models import *

from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
import random
import datetime
import jwt

from app.auth.repository import *
from app.users.repository import *


async def send_email_verifi_code(email):
    """ 
    email verification code 
    args:
        email: EmailSchema
    """
    conf = ConnectionConfig(
        MAIL_USERNAME=SETTINGS.MAIL_USERNAME,
        MAIL_PASSWORD=SETTINGS.MAIL_PASSWORD,
        MAIL_FROM=SETTINGS.MAIL_FROM,
        MAIL_PORT=SETTINGS.MAIL_PORT,
        MAIL_SERVER=SETTINGS.MAIL_SERVER,
        MAIL_STARTTLS=SETTINGS.MAIL_STARTTLS,
        MAIL_SSL_TLS=SETTINGS.MAIL_SSL_TLS,
        USE_CREDENTIALS=SETTINGS.USE_CREDENTIALS,
        VALIDATE_CERTS=SETTINGS.VALIDATE_CERTS,
        TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
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


async def create_access_token(user_email: str) -> str:
    """
    create access token
    """
    to_encode = {
        "sub": user_email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access"
    }
    access_token = jwt.encode(
        to_encode, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
    return access_token


async def create_refresh_token(user_email: str) -> str:
    """
    create refresh token
    """
    to_encode = {
        "sub": user_email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES),
        "type": "refresh"
    }
    refresh_token = jwt.encode(
        to_encode, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
    return refresh_token


async def get_current_user(request: Request):
    """
    get current user
    """
    access_token = request.cookies.get("access_token")

    if not access_token:
        return JSONResponse(content={"message": "Not authenticated"}, status_code=401)

    try:
        # jwt token 검증 이메일 반환
        payload = jwt.decode(access_token, SETTINGS.JWT_SECRET,
                             algorithms=[SETTINGS.JWT_ALGORITHM])

        email = payload.get("sub")
        if not email:
            return JSONResponse(content={"message": "Invalid token"}, status_code=401)
        return email
    except jwt.ExpiredSignatureError:
        return JSONResponse(content={"message": "Access token expired"}, status_code=401)
    except Exception as e:
        return JSONResponse(content={"message": "Invalid token"}, status_code=401)


async def create_user_by_social(user_info_data, db: AsyncSession):
    """
    create user by social
    """
    user = await create_auth_user(user_info_data, db)
    if not user:
        return JSONResponse(content={"error": "failed to create user"}, status_code=500)
    
    user_info_data['user_id'] = user.id
    profile = await create_auth_profile(user_info_data, db)
    if not profile:
        return JSONResponse(content={"error": "failed to create profile"}, status_code=500)
    
    return user, profile