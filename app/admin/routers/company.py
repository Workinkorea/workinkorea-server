from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.admin.dependencies import get_admin_user
from app.admin.services.company import AdminCompanyService
from app.admin.schemas.company import UpdateCompanyRequest, CompanyResponse
from app.auth.models import User


router = APIRouter(
    prefix="/companies",
    tags=["admin-companies"]
)


def get_admin_company_service(session: AsyncSession = Depends(get_async_session)):
    return AdminCompanyService(session)


@router.get("/", response_model=list[CompanyResponse])
async def get_all_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin_user: User = Depends(get_admin_user),
    company_service: AdminCompanyService = Depends(get_admin_company_service)
):
    """
    회사 목록 페이지네이션으로 가져옴
    """
    try:
        companies = await company_service.get_all_companies(skip, limit)
        return companies
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company_by_id(
    company_id: int,
    admin_user: User = Depends(get_admin_user),
    company_service: AdminCompanyService = Depends(get_admin_company_service)
):
    """
    회사 아이디로 하나만 가져옴
    """
    try:
        company = await company_service.get_company_by_id(company_id)
        return company
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    payload: UpdateCompanyRequest,
    admin_user: User = Depends(get_admin_user),
    company_service: AdminCompanyService = Depends(get_admin_company_service)
):
    """
    회사 수정하기
    """
    try:
        company_data = payload.model_dump(exclude_unset=True)
        updated_company = await company_service.update_company(company_id, company_data)
        return updated_company
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    admin_user: User = Depends(get_admin_user),
    company_service: AdminCompanyService = Depends(get_admin_company_service)
):
    """
    회사 삭제하기
    """
    try:
        deleted = await company_service.delete_company(company_id)
        if not deleted:
            raise ValueError("Failed to delete company")
        return JSONResponse(content={"message": "Company deleted successfully"}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
