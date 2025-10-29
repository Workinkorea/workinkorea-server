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


@router.put("")
async def update_contact(
    update_contact_request: UpdateContactRequest,
    user: User = Depends(get_current_user),
    contact_service: ContactService = Depends(get_contact_service)
) -> ContactResponse:
    """
    update current user contact
    """
    updated_contact: ContactDTO = await contact_service.update_contact(user.id, update_contact_request.model_dump())
    if not updated_contact:
        return JSONResponse(content={"error": "failed to update contact"}, status_code=400)
    return ContactResponse.model_validate(updated_contact)