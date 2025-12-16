# app/profile/routers/account_config.py
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.models import User
from app.auth.dependencies import get_current_user
from app.profile.schemas.account_config import (
    AccountConfigDTO,
    UpdateAccountConfigRequest,
    AccountConfigResponse
)
from app.profile.services.account_config import AccountConfigService


router = APIRouter(
    prefix="/account-config",
    tags=["account-config"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_account_config_service(session: AsyncSession = Depends(get_async_session)):
    return AccountConfigService(session)


@router.get("")
async def get_account_config(
    user: User = Depends(get_current_user),
    account_config_service: AccountConfigService = Depends(get_account_config_service)
) -> AccountConfigResponse:
    """
    get current user account config
    """
    account_config: AccountConfigDTO = await account_config_service.get_account_config_by_user_id(user.id)
    if not account_config:
        return JSONResponse(content={"error": "account config not found"}, status_code=404)
    return AccountConfigResponse.model_validate(account_config)


@router.patch("")
async def update_account_config(
    update_account_config_request: UpdateAccountConfigRequest,
    user: User = Depends(get_current_user),
    account_config_service: AccountConfigService = Depends(get_account_config_service)
) -> AccountConfigResponse:
    """
    update current user account config
    
    PATCH 요청 -> 일부 필드만 보내도 됨
    보내지 않은 필드는 기존 값 유지
    """
    # exclude_unset=True -> 요청에서 보내지 않은 필드는 dict에서 제외
    # exclude_none=True -> None 값도 제외 (명시적으로 None을 보내면 업데이트됨)
    update_data = update_account_config_request.model_dump(exclude_unset=True)
    
    if not update_data:
        return JSONResponse(content={"error": "no fields to update"}, status_code=400)
    
    updated_account_config: AccountConfigDTO = await account_config_service.update_account_config(user.id, update_data)
    if not updated_account_config:
        return JSONResponse(content={"error": "failed to update account config"}, status_code=400)
    return AccountConfigResponse.model_validate(updated_account_config)