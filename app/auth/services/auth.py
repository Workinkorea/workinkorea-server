# app/auth/service.py
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.core.settings import SETTINGS

from sqlalchemy.ext.asyncio import AsyncSession

from pathlib import Path
import random
import datetime
import jwt

from app.auth.repositories.auth import AuthRepository

from app.profile.repositories.profile import ProfileRepository
from app.profile.models.profile import Profile
from app.auth.models import User
from fastapi import Request
from fastapi import HTTPException

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.auth_repository = AuthRepository(session)
        self.profile_repository = ProfileRepository(session)

    async def send_email_verify_code(self, email: str):
        """ 
        email certification code 
        args:
            email: str
        """
        conf = ConnectionConfig(
            MAIL_USERNAME=SETTINGS.MAIL_USERNAME,
            MAIL_PASSWORD=SETTINGS.MAIL_PASSWORD,
            MAIL_FROM_NAME=SETTINGS.MAIL_FROM_NAME,
            MAIL_FROM=SETTINGS.MAIL_FROM,
            MAIL_PORT=SETTINGS.MAIL_PORT,
            MAIL_SERVER=SETTINGS.MAIL_SERVER,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=(Path(__file__).resolve().parents[1] / 'templates')
        )
        # random int 6 digits
        code = random.randint(100000, 999999)

        message = MessageSchema(
            subject="Work In Korea Verification Code",
            recipients=[email],
            template_body={"code": code},
            subtype=MessageType.html)

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_code_temp.html")
        return code

    async def create_access_token(self, user_email: str) -> str:
        """
        create access token
        args:
            user_email: str
        """
        try:
            to_encode = {
                "sub": user_email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES),
                "type": "access"
            }
            access_token = jwt.encode(
                to_encode, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
            return access_token
        except Exception as e:
            raise e

    async def create_refresh_token(self, user_email: str) -> str:
        """
        create refresh token
        args:
            user_email: str
        """
        try:
            to_encode = {
                "sub": user_email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES),
                "type": "refresh"
            }
            refresh_token = jwt.encode(
                to_encode, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
            return refresh_token
        except Exception as e:
            raise e

    async def get_current_user(self, request: Request) -> User | None:
        """
        get current user
        """
        access_token = request.cookies.get("access_token")

        if not access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        try:
            # jwt token 검증 이메일 반환
            payload = jwt.decode(access_token, SETTINGS.JWT_SECRET,
                                algorithms=[SETTINGS.JWT_ALGORITHM])

            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid token")
            return email
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token expired")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def create_user_by_social(self, user_info_data: dict) -> tuple[User, Profile] | None:
        """
        create user by social
        args:
            user_info_data: dict
        """
        user = await self.auth_repository.create_user_by_social(user_info_data)
        if not user:
            return None
        
        # profile 생성
        user_info_data['user_id'] = user.id
        profile = await self.profile_repository.create_profile(user_info_data)
        if not profile:
            return None
        
        return user, profile

    async def get_user_by_email(self, email: str) -> User | None:
        """
        get user by email
        args:
            email: str
        """
        return await self.auth_repository.get_user_by_email(email)

    async def update_user_company_info(self, email: str, company_info: dict) -> User | None:
        """
        update company user
        args:
            user_id: int
            company_info: dict
        """
        return await self.auth_repository.update_user_company_info(email, company_info)