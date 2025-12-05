from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.models.company_profile import CompanyProfile
from sqlalchemy import select, insert, update


class CompanyProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_company_profile_by_company_id(self, company_id: int) -> CompanyProfile | None:
        """
        get company profile by company id
        args:
            company_id: int
        """
        try:
            stmt = select(CompanyProfile).where(CompanyProfile.company_id == company_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def create_company_profile_to_db(self, company_profile_data: dict) -> CompanyProfile | None:
        """
        create company profile to db
        args:
            company_profile_data: dict
        """
        try:
            stmt = insert(CompanyProfile).values(company_profile_data).returning(CompanyProfile)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def update_company_profile_to_db(self, company_profile_data: dict) -> CompanyProfile | None:
        """
        update company profile to db
        args:
            company_profile_data: dict
        """
        try:
            stmt = update(CompanyProfile).values(company_profile_data).where(CompanyProfile.company_id == company_profile_data['company_id']).returning(CompanyProfile)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e