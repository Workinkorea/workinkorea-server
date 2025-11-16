from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.posts.services.company_post import CompanyPostService
from app.auth.services.company import CompanyService
from app.profile.services.position import PositionService

from app.posts.schemas.request import CompanyPostRequest
from app.posts.schemas.response import CompanyPostResponse

router = APIRouter(
    prefix="/company",
    tags=["company-post"]
)

def get_company_post_service(session: AsyncSession = Depends(get_async_session)):
    return CompanyPostService(session)

def get_company_service(session: AsyncSession = Depends(get_async_session)):
    return CompanyService(session)

def get_position_service(session: AsyncSession = Depends(get_async_session)):
    return PositionService(session)

@router.get("/")
async def get_list_company_posts(
    request: Request,
    company_post_service: CompanyPostService = Depends(get_company_post_service),
    company_service: CompanyService = Depends(get_company_service)
):
    """
    get company post
    """
    try:
        company = await company_service.get_current_company(request)
        if not company:
            return JSONResponse(content={"error": "Company not found"}, status_code=404)
        company_posts = await company_post_service.get_list_company_posts_by_company_id(company.id)

        return JSONResponse(content={"company_posts": company_posts}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/{company_post_id}")
async def get_company_post_by_company_post_id(
    company_post_id: int,
    company_post_service: CompanyPostService = Depends(get_company_post_service),
):
    """
    get company post
    """
    try:
        company_post = await company_post_service.get_company_post_by_company_post_id(company_post_id)
        return CompanyPostResponse.model_validate(company_post)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/")
async def create_company_post(
    request: Request,
    payload: CompanyPostRequest,
    company_post_service: CompanyPostService = Depends(get_company_post_service),
    company_service: CompanyService = Depends(get_company_service),
    position_service: PositionService = Depends(get_position_service)
):
    """
    create company post
    """
    try:
        company = await company_service.get_current_company(request)
        if not company:
            return JSONResponse(content={"error": "Company not found"}, status_code=404)
        company_post_data = payload.model_dump()
        company_post_data['company_id'] = company.id
        position = await position_service.get_position_by_position_id(company_post_data['position_id'])
        if not position:
            return JSONResponse(content={"error": "Position not found"}, status_code=404)
        company_post_data['position_id'] = position.id
        company_post = await company_post_service.create_company_post(company_post_data)
        return CompanyPostResponse.model_validate(company_post)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.put("/{company_post_id}")
async def update_company_post(
    request: Request,
    company_post_id: int,
    payload: CompanyPostRequest,
    company_post_service: CompanyPostService = Depends(get_company_post_service),
    company_service: CompanyService = Depends(get_company_service),
    position_service: PositionService = Depends(get_position_service)
):
    """
    update company post
    """
    try:
        company = await company_service.get_current_company(request)
        if not company:
            return JSONResponse(content={"error": "Company not found"}, status_code=404)
        company_post_data = payload.model_dump()
        company_post_data['company_id'] = company.id
        position = await position_service.get_position_by_position_id(company_post_data['position_id'])
        if not position:
            return JSONResponse(content={"error": "Position not found"}, status_code=404)
        company_post_data['position_id'] = position.id
        company_post_data['id'] = company_post_id
        company_post = await company_post_service.update_company_post(company_post_data)
        return CompanyPostResponse.model_validate(company_post)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.delete("/{company_post_id}")
async def delete_company_post(
    request: Request,
    company_post_id: int,
    company_post_service: CompanyPostService = Depends(get_company_post_service),
    company_service: CompanyService = Depends(get_company_service)
):
    """
    delete company post
    """
    try:
        company = await company_service.get_current_company(request)
        if not company:
            raise ValueError("Company not found")
        deleted = await company_post_service.delete_company_post(company_post_id)
        if not deleted:
            raise ValueError("Failed to delete company post")
        return JSONResponse(content={"message": "Company post deleted"}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)