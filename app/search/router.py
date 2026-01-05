from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.admin.services.company import AdminCompanyService
from app.admin.schemas.company import CompanyResponse

router = APIRouter(
    prefix="/companies",
    tags=["search"]
)


def get_company_service(session: AsyncSession = Depends(get_async_session)):
    return AdminCompanyService(session)


@router.get("/", response_model=list[CompanyResponse])
async def get_all_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    company_service: AdminCompanyService = Depends(get_company_service)
):
    """
    회사 목록 조회 (일반 사용자용)
    """
    try:
        companies = await company_service.get_all_companies(skip, limit)
        return companies
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company_by_id(
    company_id: int,
    company_service: AdminCompanyService = Depends(get_company_service)
):
    """
    회사 상세 조회 (일반 사용자용)
    """
    try:
        company = await company_service.get_company_by_id(company_id)
        return company
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
