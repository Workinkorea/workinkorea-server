from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.models.company_profile import CompanyProfile
from app.profile.repositories.company_profile import CompanyProfileRepository
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from app.profile.schemas.company_profile import CompanyProfileDTO
from app.auth.repositories.company import CompanyRepository

class CompanyProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_profile_repository = CompanyProfileRepository(session)
        self.company_repository = CompanyRepository(session)

    async def get_company_profile_by_company_id(self, company_id: int) -> CompanyProfileDTO:
        """
        get company profile by company id
        args:
            company_id: int
        """
        company_profile = await self.company_profile_repository.get_company_profile_by_company_id(company_id)
        if not company_profile:
            raise ValueError("company profile not found")
        return CompanyProfileDTO.model_validate(company_profile)

    async def create_company_profile_to_db(self, company_profile_data: dict):
        """
        create company profile to db
        args:
            company_profile_data: dict
        """
        company_profile = await self.company_profile_repository.create_company_profile_to_db(company_profile_data)
        if not company_profile:
            raise ValueError("failed to create company profile")
        return CompanyProfileDTO.model_validate(company_profile)

    async def update_company_profile_to_db(self, company_profile_data: dict):
        """
        update company profile to db
        args:
            company_profile_data: dict
        """
        company_profile = await self.company_profile_repository.get_company_profile_by_company_id(company_profile_data['company_id'])
        if not company_profile:
            raise ValueError("company profile not found")

        if company_profile.industry_type == company_profile_data['industry_type'] and \
            company_profile.employee_count == company_profile_data['employee_count'] and \
            company_profile.establishment_date == company_profile_data['establishment_date'] and \
            company_profile.company_type == company_profile_data['company_type'] and \
            company_profile.insurance == company_profile_data['insurance'] and \
            company_profile.phone_number == company_profile_data['phone_number'] and \
            company_profile.address == company_profile_data['address'] and \
            company_profile.website_url == company_profile_data['website_url'] and \
            company_profile.email == company_profile_data['email']:
            raise ValueError("company profile is the same")


        company_profile = await self.company_profile_repository.update_company_profile_to_db(company_profile_data)
        if not company_profile:
            raise ValueError("failed to update company profile")
        return CompanyProfileDTO.model_validate(company_profile)