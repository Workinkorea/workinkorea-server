# app/profile/routers/profile.py
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.models import User
from app.auth.dependencies import get_current_user
from app.profile.schemas.profile import ProfileDTO, UpdateProfileRequest, ProfileResponse, UserImageRequest
from app.profile.services.profile import ProfileService

from app.core.minio_handles import MinioHandles

router = APIRouter(
    prefix="/me",
    tags=["me"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_profile_service(session: AsyncSession = Depends(get_async_session)):
    return ProfileService(session)

def get_minio_handles() -> MinioHandles:
    return MinioHandles()

@router.get("")
async def get_profile(
    user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service)
) -> ProfileResponse:
    """
    get current user profile
    """
    profile: ProfileDTO | None = await profile_service.get_profile_by_user_id(user.id)
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
    updated_profile: ProfileDTO | None = await profile_service.update_profile(user.id, update_profile_request.model_dump())
    if not updated_profile:
        return JSONResponse(content={"error": "failed to update profile"}, status_code=400)
    return ProfileResponse.model_validate(updated_profile)


@router.post("test/user/image")
async def test_user_image(
    user_image_request: UserImageRequest,
    user: User = Depends(get_current_user),
    minio_handles: MinioHandles = Depends(get_minio_handles)
) -> JSONResponse:
    """
    test user image
    """
    file_data = user_image_request.model_dump()
    file_url_data = minio_handles.upload_resume_file(user.id, file_data['file_name'], "user_image", "image/jpeg")
    return JSONResponse(content={"minio_test": file_url_data}, status_code=200)