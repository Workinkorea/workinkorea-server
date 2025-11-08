# app/auth/router.py
from fastapi.responses import JSONResponse
from fastapi import Request, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.services.auth import AuthService
from app.auth.models import User
from app.profile.schemas.request import *
from app.profile.schemas.response import *
from app.profile.schemas.profile import ProfileDTO
from app.profile.services.profile import ProfileService


router = APIRouter(
    prefix="/profile",
    tags=["profile"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_profile_service(session: AsyncSession = Depends(get_async_session)):
    return ProfileService(session)


def get_auth_service(session: AsyncSession = Depends(get_async_session)):
    return AuthService(session)


@router.get("")
async def get_profile(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    profile_service: ProfileService = Depends(get_profile_service)
) -> ProfileResponse:
    """
    get current user profile
    """
    user: User = await auth_service.get_current_user(request)
    profile: ProfileDTO = await profile_service.get_profile_by_user_id(user.id)
    if not profile:
        return JSONResponse(content={"error": "profile not found"}, status_code=404)
    return ProfileResponse(
        profile_image_url=profile.profile_image_url,
        location=profile.location,
        introduction=profile.introduction,
        position_id=profile.position_id,
        job_status=profile.job_status,
        portfolio_url=profile.portfolio_url,
        birth_date=profile.birth_date,
        name=profile.name,
        country_id=profile.country_id,
    )


@router.put("")
async def update_profile(
    request: UpdateProfileRequest,
    data: UpdateProfileRequest,
    auth_service: AuthService = Depends(get_auth_service),
    profile_service: ProfileService = Depends(get_profile_service)
) -> ProfileResponse:
    """
    update current user profile
    """
    user: User = await auth_service.get_current_user(request)
    profile: ProfileDTO = await profile_service.get_profile_by_user_id(user.id)
    if not profile:
        return JSONResponse(content={"error": "profile not found"}, status_code=404)
    updated = await profile_service.update_profile(user.id, data.model_dump())
    if not updated:
        return JSONResponse(content={"error": "failed to update profile"}, status_code=400)
    return ProfileResponse(
        profile_image_url=profile.profile_image_url,
        location=profile.location,
        introduction=profile.introduction,
        position_id=profile.position_id,
        job_status=profile.job_status,
        portfolio_url=profile.portfolio_url,
        birth_date=profile.birth_date,
        name=profile.name,
        country_id=profile.country_id,
    )