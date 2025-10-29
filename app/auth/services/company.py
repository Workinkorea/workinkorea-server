from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.repositories.company import CompanyRepository
from app.auth.models import Company, CompanyUser
from fastapi.responses import JSONResponse
import hashlib


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
            return JSONResponse(content={"error": "Company user not found"}, status_code=404)

        password_hash = hashlib.sha256(company_user_data['password'].encode('utf-8')).hexdigest()
        if password_hash != company_user.password:
            return JSONResponse(content={"error": "Invalid password"}, status_code=400)
        
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