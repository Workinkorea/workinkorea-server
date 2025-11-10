from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from fastapi.responses import JSONResponse

from app.profile.services.company_profile import CompanyProfileService
from app.profile.schemas.company_profile import CompanyProfileResponse
from app.profile.schemas.company_profile import CompanyProfileRequest
from app.auth.services.company import CompanyService

router = APIRouter(
    prefix='/company-profile',
    tags=["company-profile"]
)

def get_company_profile_service(session:AsyncSession = Depends(get_async_session)):
    return CompanyProfileService(session)

def get_company_service(session: AsyncSession = Depends(get_async_session)):
    return CompanyService(session)

@router.get("")
async def get_company_profile(
    request: Request,
    company_profile_service: CompanyProfileService = Depends(get_company_profile_service),
    company_service: CompanyService = Depends(get_company_service)
) -> CompanyProfileResponse:
    """
    get company profile
    """
    try:
        company = await company_service.get_current_company(request)
        if not company:
            return JSONResponse(content={"error": "company not found"}, status_code=404)    
        company_profile = await company_profile_service.get_company_profile_by_company_id(company.id)
        return CompanyProfileResponse(
            industry_type=company_profile.industry_type,
            employee_count=company_profile.employee_count,
            establishment_date=company_profile.establishment_date,
            company_type=company_profile.company_type,
            insurance=company_profile.insurance,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.post("")
async def create_company_profile(
    request: Request,
    payload: CompanyProfileRequest,
    company_profile_service: CompanyProfileService = Depends(get_company_profile_service),
    company_service: CompanyService = Depends(get_company_service)
) -> CompanyProfileResponse:
    """
    create company profile
    """
    try:
        company_profile_data = payload.model_dump()
        company = await company_service.get_current_company(request)
        company_profile_data['company_id'] = company.id
        company_profile = await company_profile_service.create_company_profile_to_db(company_profile_data)
        return CompanyProfileResponse(
            company_id=company_profile.company_id,
            industry_type=company_profile.industry_type,
            employee_count=company_profile.employee_count,
            establishment_date=company_profile.establishment_date,
            company_type=company_profile.company_type,
            insurance=company_profile.insurance,
            phone_number=company_profile.phone_number,
            address=company_profile.address,
            website_url=company_profile.website_url,
            email=company_profile.email,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.put("")
async def update_company_profile(
    request: Request,
    payload: CompanyProfileRequest,
    company_profile_service: CompanyProfileService = Depends(get_company_profile_service),
    company_service: CompanyService = Depends(get_company_service)
) -> CompanyProfileResponse:
    """
    update company profile
    """
    try:
        company_profile_data = payload.model_dump()
        company = await company_service.get_current_company(request)
        company_profile_data['company_id'] = company.id
        company_profile = await company_profile_service.update_company_profile_to_db(company_profile_data)
        return CompanyProfileResponse(
            company_id=company_profile.company_id,
            industry_type=company_profile.industry_type,
            employee_count=company_profile.employee_count,
            establishment_date=company_profile.establishment_date,
            company_type=company_profile.company_type,
            insurance=company_profile.insurance,
            phone_number=company_profile.phone_number,
            address=company_profile.address,
            website_url=company_profile.website_url,
            email=company_profile.email,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)