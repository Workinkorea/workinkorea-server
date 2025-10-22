# app/auth/router.py
from fastapi.responses import JSONResponse
from fastapi import Request, APIRouter, Depends


from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.service import *
from app.auth.schemas.request import *
from app.users.service import UsersService


router = APIRouter(
    prefix="/api/users",
    tags=["auth"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_users_service(session: AsyncSession = Depends(get_async_session)):
    return UsersService(session)


@router.get("/profile")
async def get_profile(request: Request, users_service: UsersService = Depends(get_users_service)):
    """
    get current user profile
    """
    user = await users_service.get_current_user(request)
    profile = await users_service.get_profile_by_user_id(user.id)
    return JSONResponse(content={"message": "Hello, World!"})