# python
import jwt
import random
import datetime
from pathlib import Path
from typing import Optional

# app/core
from app.core.settings import SETTINGS

# app/auth
from app.auth.models import User
from app.auth.schemas.user import UserDTO
from app.auth.repositories.auth import AuthRepository

# app/profile
from app.profile.models.contact import Contact
from app.profile.models.profile import Profile
from app.profile.schemas.profile import ProfileDTO
from app.profile.schemas.contact import ContactDTO
from app.profile.models.account_config import AccountConfig
from app.profile.repositories.profile import ProfileRepository
from app.profile.repositories.contact import ContactRepository
from app.profile.schemas.account_config import AccountConfigDTO
from app.profile.repositories.account_config import AccountConfigRepository

# sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

# fastapi
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.auth_repository = AuthRepository(session)
        self.profile_repository = ProfileRepository(session)
        self.contact_repository = ContactRepository(session)
        self.account_config_repository = AccountConfigRepository(session)

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

    async def create_admin_access_token(self, user_email: str) -> str:
        """
        어드민 전용 토큰 만들기
        args:
            user_email: str
        """
        try:
            to_encode = {
                "sub": user_email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES),
                "type": "admin_access"
            }
            admin_access_token = jwt.encode(
                to_encode, SETTINGS.ADMIN_JWT_SECRET, algorithm=SETTINGS.ADMIN_JWT_ALGORITHM)
            return admin_access_token
        except Exception as e:
            raise e

    async def create_admin_refresh_token(self, user_email: str) -> str:
        """
        어드민 전용 리프레시 토큰 만들기
        args:
            user_email: str
        """
        try:
            to_encode = {
                "sub": user_email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.ADMIN_REFRESH_TOKEN_EXPIRE_MINUTES),
                "type": "admin_refresh"
            }
            admin_refresh_token = jwt.encode(
                to_encode, SETTINGS.ADMIN_JWT_SECRET, algorithm=SETTINGS.ADMIN_JWT_ALGORITHM)
            return admin_refresh_token
        except Exception as e:
            raise e

    # async def get_current_user(self, request: Request) -> User | JSONResponse:
    #     """
    #     get current user
    #     args:
    #         request: Request
    #     """
    #     access_token = request.cookies.get("access_token")

    #     if not access_token:
    #         return JSONResponse(content={"message": "Not authenticated"}, status_code=401)

    #     try:
    #         # jwt token 검증 이메일 반환
    #         payload = jwt.decode(access_token, SETTINGS.JWT_SECRET,
    #                             algorithms=[SETTINGS.JWT_ALGORITHM])

    #         email = payload.get("sub")
    #         if not email:
    #             return JSONResponse(content={"message": "Invalid token"}, status_code=401)
    #         user = await self.auth_repository.get_user_by_email(email)
    #         if not user:
    #             return JSONResponse(content={"message": "User not found"}, status_code=404)
    #         return user
    #     except jwt.ExpiredSignatureError:
    #         return JSONResponse(content={"message": "Access token expired"}, status_code=401)
    #     except Exception as e:
    #         return JSONResponse(content={"message": "Invalid token"}, status_code=401)

    async def create_user_by_social(
        self,
        user_info_data: dict
    ) -> tuple[UserDTO, ProfileDTO, ContactDTO, AccountConfigDTO] :
        """
        create user by social
        args:
            user_info_data: dict
        """
        user: Optional[User] = await self.auth_repository.create_user_by_social(user_info_data)
        if not user:
            raise ValueError("failed to create user")
        
        # profile 생성
        user_info_data['user_id'] = user.id
        profile: Optional[Profile] = await self.profile_repository.create_profile(user_info_data)
        if not profile:
            raise ValueError("failed to create profile")

        contact: Optional[Contact] = await self.contact_repository.create_contact(
            profile.user_id, {
                'phone_number': None,
                'github_url': None,
                'linkedin_url': None,
                'website_url': None,
            })
        if not contact:
            raise ValueError("failed to create contact")

        account_config: Optional[AccountConfig] = await self.account_config_repository.create_account_config(
            profile.user_id, {
                'sns_message_notice': True,
                'email_notice': True,
            })
        if not account_config:
            raise ValueError("failed to create account config")
        
        return UserDTO.model_validate(user), ProfileDTO.model_validate(profile), ContactDTO.model_validate(contact), AccountConfigDTO.model_validate(account_config)

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