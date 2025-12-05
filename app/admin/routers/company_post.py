from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.admin.dependencies import get_admin_user
from app.admin.services.company_post import AdminCompanyPostService
from app.admin.schemas.company_post import UpdateCompanyPostRequest, CompanyPostResponse
from app.auth.models import User


router = APIRouter(
    prefix="/posts",
    tags=["admin-posts"]
)


def get_admin_company_post_service(session: AsyncSession = Depends(get_async_session)):
    return AdminCompanyPostService(session)


@router.get("/", response_model=list[CompanyPostResponse])
async def get_all_company_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin_user: User = Depends(get_admin_user),
    post_service: AdminCompanyPostService = Depends(get_admin_company_post_service)
):
    """
    회사 공고 목록 페이지네이션으로 가져옴
    """
    try:
        posts = await post_service.get_all_company_posts(skip, limit)
        return posts
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/{post_id}", response_model=CompanyPostResponse)
async def get_company_post_by_id(
    post_id: int,
    admin_user: User = Depends(get_admin_user),
    post_service: AdminCompanyPostService = Depends(get_admin_company_post_service)
):
    """
    회사 공고 아이디로 하나만 가져옴
    """
    try:
        post = await post_service.get_company_post_by_id(post_id)
        return post
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.put("/{post_id}", response_model=CompanyPostResponse)
async def update_company_post(
    post_id: int,
    payload: UpdateCompanyPostRequest,
    admin_user: User = Depends(get_admin_user),
    post_service: AdminCompanyPostService = Depends(get_admin_company_post_service)
):
    """
    회사 공고 수정하기
    """
    try:
        post_data = payload.model_dump(exclude_unset=True)
        updated_post = await post_service.update_company_post(post_id, post_data)
        return updated_post
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/{post_id}")
async def delete_company_post(
    post_id: int,
    admin_user: User = Depends(get_admin_user),
    post_service: AdminCompanyPostService = Depends(get_admin_company_post_service)
):
    """
    회사 공고 삭제하기
    """
    try:
        deleted = await post_service.delete_company_post(post_id)
        if not deleted:
            raise ValueError("Failed to delete company post")
        return JSONResponse(content={"message": "Company post deleted successfully"}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
