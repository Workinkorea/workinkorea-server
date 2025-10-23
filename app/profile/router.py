# app/auth/router.py
from fastapi.responses import JSONResponse
from fastapi import Request, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.service import *
from app.profile.service import ProfileService
from app.profile.schemas.request import *


router = APIRouter(
    prefix="/api/profile",
    tags=["auth"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_profile_service(session: AsyncSession = Depends(get_async_session)):
    return ProfileService(session)


def get_auth_service(session: AsyncSession = Depends(get_async_session)):
    return AuthService(session)


@router.get("/profile")
async def get_profile(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    profile_service: ProfileService = Depends(get_profile_service)
):
    """
    get current user profile
    """
    user: User = await auth_service.get_current_user(request)
    profile: Profile = await profile_service.get_profile_by_user_id(user.id)
    return JSONResponse(content={"message": "Hello, World!"})