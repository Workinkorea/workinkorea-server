# app/auth/router.py
from fastapi.responses import JSONResponse
from fastapi import Request, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.services.auth import AuthService
from app.auth.models import User
from app.profile.schemas.request import *
from app.profile.schemas.response import *
from app.profile.schemas.account_config import AccountConfigDTO
from app.profile.services.account_config import AccountConfigService
 

router = APIRouter(
    prefix="/profile/account-config",
    tags=["account-config"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_account_config_service(session: AsyncSession = Depends(get_async_session)):
    return AccountConfigService(session)


def get_auth_service(session: AsyncSession = Depends(get_async_session)):
    return AuthService(session)


@router.get("")
async def get_account_config(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    account_config_service: AccountConfigService = Depends(get_account_config_service)
) -> AccountConfigResponse:
    """
    get current user account config
    """
    user: User = await auth_service.get_current_user(request)
    account_config: AccountConfigDTO = await account_config_service.get_account_config_by_user_id(user.id)
    if not account_config:
        return JSONResponse(content={"error": "account config not found"}, status_code=404)
    return AccountConfigResponse(
        sns_message_notice=account_config.sns_message_notice,
        email_notice=account_config.email_notice
    )
