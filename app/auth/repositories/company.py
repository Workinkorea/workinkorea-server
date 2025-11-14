from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from app.auth.models import Company, CompanyUser
from app.core.settings import SETTINGS


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_company_by_company_number(self, company_number: str) -> Company | None:
        """
        get company by company number
        args:
            company_number: str
        """
        try:
            stmt = select(Company).where(Company.company_number == company_number)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def create_company_to_db(self, company_data: dict) -> Company | None:
        """
        create company to db
        args:
            company_info_data: dict
        """
        try:
            stmt = insert(Company).values(
                company_number=company_data['company_number'],
                company_name=company_data['company_name'],
            ).returning(Company)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def get_company_user_by_email(self, email: str) -> CompanyUser | None:
        """
        get company user by email
        args:
            email: str
        """
        try:
            stmt = select(CompanyUser).where(CompanyUser.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def create_company_user_to_db(self, user_data: dict) -> CompanyUser | None:
        """
        create company user to db
        args:
            user_data: dict
        """
        try:
            stmt = insert(CompanyUser).values(
                company_id=user_data['company_id'],
                email=user_data['email'],
                password=user_data['password'],
                name=user_data['name'],
                phone=user_data['phone']
            ).returning(CompanyUser)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except Exception as e:
            raise e

    async def get_company_by_company_id(self, company_id: int) -> Company | None:
        """
        get company by company id
        args:
            company_id: int
        """
        try:
            stmt = select(Company).where(Company.id == company_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e