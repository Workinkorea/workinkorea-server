# app/profile/routers/contact.py
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.dependencies import get_current_user
from app.profile.schemas.contact import ContactDTO, UpdateContactRequest, ContactResponse
from app.profile.services.contact import ContactService


router = APIRouter(
    prefix="/contact",
    tags=["contact"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_contact_service(session: AsyncSession = Depends(get_async_session)):
    return ContactService(session)


@router.get("")
async def get_contact(
    user: User = Depends(get_current_user),
    contact_service: ContactService = Depends(get_contact_service)
) -> ContactResponse:
    """
    get current user contact
    """
    contact: ContactDTO = await contact_service.get_contact_by_user_id(user.id)
    if not contact:
        return JSONResponse(content={"error": "contact not found"}, status_code=404)
    return ContactResponse.model_validate(contact)


@router.patch("")
async def update_contact(
    update_contact_request: UpdateContactRequest,
    user: User = Depends(get_current_user),
    contact_service: ContactService = Depends(get_contact_service)
) -> ContactResponse:
    """
    update current user contact

    PATCH 요청 -> 일부 필드만 보내도 됨
    보내지 않은 필드는 기존 값 유지
    """
    # exclude_unset=True -> 요청에서 보내지 않은 필드는 dict에서 제외
    # exclude_none=True -> None 값도 제외 (명시적으로 None을 보내면 업데이트됨)
    update_data = update_contact_request.model_dump(exclude_unset=True)
    
    if not update_data:
        return JSONResponse(content={"error": "no fields to update"}, status_code=400)
    
    updated_contact: ContactDTO = await contact_service.update_contact(user.id, update_data)
    if not updated_contact:
        return JSONResponse(content={"error": "failed to update contact"}, status_code=400)
    return ContactResponse.model_validate(updated_contact)