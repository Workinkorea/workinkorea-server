from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.repositories.company import CompanyRepository
from app.auth.models import Company

class CompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_repository = CompanyRepository(session)

    async def create_company_to_db(self, company_data: dict) -> Company | None:
        """
        create company to db
        args:
        """
        return await self.company_repository.create_company_to_db(company_data)