# python
import jwt
import random
import datetime
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


import json
import base64
import asyncio
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build



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
        code = random.randint(100000, 999999)

        # 서비스 계정 인증 (JSON 또는 Base64 인코딩된 JSON 지원)
        try:
            service_account_info = json.loads(SETTINGS.GMAIL_SERVICE_ACCOUNT_JSON)
        except json.JSONDecodeError:
            service_account_info = json.loads(base64.b64decode(SETTINGS.GMAIL_SERVICE_ACCOUNT_JSON).decode())
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/gmail.send"],
            subject=SETTINGS.GMAIL_DELEGATED_USER
        )
        service = build("gmail", "v1", credentials=creds)

        # HTML 템플릿 렌더링
        template_path = Path(__file__).resolve().parents[1] / 'templates' / 'email_code_temp.html'
        html_content = template_path.read_text().replace("{{ code }}", str(code))

        # 이메일 생성
        msg = MIMEMultipart()
        msg["to"] = email
        msg["from"] = SETTINGS.GMAIL_FROM
        msg["subject"] = "Work In Korea Verification Code"
        msg.attach(MIMEText(html_content, "html"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        await asyncio.to_thread(
            service.users().messages().send(userId="me", body={"raw": raw}).execute
        )

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