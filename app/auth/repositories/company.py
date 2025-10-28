from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from app.auth.models import Company
from app.core.settings import SETTINGS


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_company_to_db(self, company_data: dict) -> Company | None:
        """
        create company to db
        args:
            company_info_data: dict
        """
        try:
            stmt = insert(Company).values(
                company_number=company_data['company_number'],
                company_name=company_data['company_name']
            ).returning(Company)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except Exception as e:
            raise e