from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.repositories.company import CompanyRepository
from app.auth.models import Company, CompanyUser
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import hashlib

from app.core.settings import SETTINGS
import datetime
import jwt


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_repository = CompanyRepository(session)

    async def get_company_by_company_number(self, company_number: int) -> Company | None:
        """
        get company by company number
        args:
            company_number: int
        """
        return await self.company_repository.get_company_by_company_number(company_number)

    async def create_company_to_db(self, company_data: dict) -> Company | None:
        """
        create company to db
        """
        return await self.company_repository.create_company_to_db(company_data)
    
    async def company_user_login(self, company_user_data: dict) -> CompanyUser | None:
        """
        get company user by email
        """
        company_user = await self.company_repository.get_company_user_by_email(company_user_data['email'])

        if not company_user:
            return None

        password_hash = hashlib.sha256(company_user_data['password'].encode('utf-8')).hexdigest()
        if password_hash != company_user.password:
            return None
        
        return company_user


    async def create_company_user_to_db(self, company_user_data: dict) -> CompanyUser | None:
        """
        create company user to db
        args:
            user_data: dict
        """
        # password hash
        company_user_data['password'] = hashlib.sha256(company_user_data['password'].encode('utf-8')).hexdigest()
        return await self.company_repository.create_company_user_to_db(company_user_data)

    async def create_access_company_token(self, user_email: str, company_id: int) -> str:
        """
        create access company token
        args:
            user_email: str
        """
        try:
            to_encode = {
                "sub": user_email,
                "company_id": company_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES),
                "type": "access_company"
            }
            access_token = jwt.encode(
                to_encode, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
            return access_token
        except Exception as e:
            raise e

    async def create_refresh_company_token(self, user_email: str, company_id: int) -> str:
        """
        create refresh company token
        args:
            user_email: str
        """
        try:
            to_encode = {
                "sub": user_email,
                "company_id": company_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES),
                "type": "refresh_company"
            }
            refresh_token = jwt.encode(
                to_encode, SETTINGS.JWT_SECRET, algorithm=SETTINGS.JWT_ALGORITHM)
            return refresh_token
        except Exception as e:
            raise e