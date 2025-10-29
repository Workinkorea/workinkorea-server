# app/profile/routers/profile.py
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.models import User
from app.auth.dependencies import get_current_user
from app.profile.schemas.profile import ProfileDTO, UpdateProfileRequest, ProfileResponse
from app.profile.services.profile import ProfileService


router = APIRouter(
    prefix="/me",
    tags=["me"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_profile_service(session: AsyncSession = Depends(get_async_session)):
    return ProfileService(session)


@router.get("")
async def get_profile(
    user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service)
) -> ProfileResponse:
    """
    get current user profile
    """
    profile: ProfileDTO = await profile_service.get_profile_by_user_id(user.id)
    if not profile:
        return JSONResponse(content={"error": "profile not found"}, status_code=404)
    return ProfileResponse.model_validate(profile)


@router.put("")
async def update_profile(
    update_profile_request: UpdateProfileRequest,
    user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service)
) -> ProfileResponse:
    """
    update current user profile
    """
    updated_profile: ProfileDTO = await profile_service.update_profile(user.id, update_profile_request.model_dump())
    if not updated_profile:
        return JSONResponse(content={"error": "failed to update profile"}, status_code=400)
    return ProfileResponse.model_validate(updated_profile)