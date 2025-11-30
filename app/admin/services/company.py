from sqlalchemy.ext.asyncio import AsyncSession
from app.admin.repositories.company import AdminCompanyRepository
from app.admin.schemas.company import CompanyResponse


class AdminCompanyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_repository = AdminCompanyRepository(session)

    async def get_all_companies(self, skip: int = 0, limit: int = 100) -> list[CompanyResponse]:
        """
        Get all companies with pagination
        """
        companies = await self.company_repository.get_all_companies(skip, limit)
        return [CompanyResponse.model_validate(company) for company in companies]

    async def get_company_by_id(self, company_id: int) -> CompanyResponse | None:
        """
        Get company by id
        """
        company = await self.company_repository.get_company_by_id(company_id)
        if not company:
            raise ValueError("Company not found")
        return CompanyResponse.model_validate(company)

    async def update_company(self, company_id: int, company_data: dict) -> CompanyResponse:
        """
        Update company
        """
        existing_company = await self.company_repository.get_company_by_id(company_id)
        if not existing_company:
            raise ValueError("Company not found")

        updated_company = await self.company_repository.update_company(company_id, company_data)
        if not updated_company:
            raise ValueError("Failed to update company")
        return CompanyResponse.model_validate(updated_company)

    async def delete_company(self, company_id: int) -> bool:
        """
        Delete company
        """
        company = await self.company_repository.get_company_by_id(company_id)
        if not company:
            raise ValueError("Company not found")

        return await self.company_repository.delete_company(company)
