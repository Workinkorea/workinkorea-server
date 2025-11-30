from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.admin.dependencies import get_admin_user
from app.admin.services.user import AdminUserService
from app.admin.schemas.user import UpdateUserRequest, UserResponse
from app.auth.models import User


router = APIRouter(
    prefix="/users",
    tags=["admin-users"]
)


def get_admin_user_service(session: AsyncSession = Depends(get_async_session)):
    return AdminUserService(session)


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin_user: User = Depends(get_admin_user),
    user_service: AdminUserService = Depends(get_admin_user_service)
):
    """
    유저 목록 페이지네이션으로 가져옴
    """
    try:
        users = await user_service.get_all_users(skip, limit)
        return users
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    user_service: AdminUserService = Depends(get_admin_user_service)
):
    """
    유저 아이디로 하나만 가져옴
    """
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    payload: UpdateUserRequest,
    admin_user: User = Depends(get_admin_user),
    user_service: AdminUserService = Depends(get_admin_user_service)
):
    """
    유저 수정하기
    """
    try:
        user_data = payload.model_dump(exclude_unset=True)
        updated_user = await user_service.update_user(user_id, user_data)
        return updated_user
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    user_service: AdminUserService = Depends(get_admin_user_service)
):
    """
    유저 삭제하기
    """
    try:
        deleted = await user_service.delete_user(user_id)
        if not deleted:
            raise ValueError("Failed to delete user")
        return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
