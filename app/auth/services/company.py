from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.repositories.company import CompanyRepository
from app.auth.models import Company, CompanyUser
from fastapi import HTTPException, Request
import hashlib

from app.core.settings import SETTINGS
import datetime
import jwt


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_repository = CompanyRepository(session)

    async def get_company_by_company_number(self, company_number: str) -> Company | None:
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
            raise ValueError("company user not found")

        password_hash = hashlib.sha256(company_user_data['password'].encode('utf-8')).hexdigest()
        if password_hash != company_user.password:
            raise ValueError("password is incorrect")
        
        return company_user

    async def get_company_user_by_email(self, email: str, company_id: int) -> CompanyUser | None:
        """
        get company user by email
        args:
            email: str
        """
        return await self.company_repository.get_company_user_by_email(email, company_id)


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

    async def get_current_company(self, request:Request) -> Company | None:
        """
        get current company
        args:
            request: Request
        """
        access_token = request.cookies.get("access_token")

        if not access_token:
            raise ValueError("Not authenticated")
        
        payload = jwt.decode(access_token, SETTINGS.JWT_SECRET, algorithms=[SETTINGS.JWT_ALGORITHM])
        company_id = payload.get("company_id")
        if not company_id:
            raise ValueError("Company ID not found")

        return await self.company_repository.get_company_by_company_id(int(company_id))