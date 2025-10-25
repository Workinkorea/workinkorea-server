# app/auth/router.py
from fastapi.responses import JSONResponse
from fastapi import Request, APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.service import *
from app.profile.schemas.request import *
from app.profile.schemas.response import *
from app.profile.schemas.contact import ContactDTO
from app.profile.services.contact import ContactService


router = APIRouter(
    prefix="/contact",
    tags=["contact"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_contact_service(session: AsyncSession = Depends(get_async_session)):
    return ContactService(session)


def get_auth_service(session: AsyncSession = Depends(get_async_session)):
    return AuthService(session)


@router.get("/contact")
async def get_contact(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    contact_service: ContactService = Depends(get_contact_service)
) -> ContactResponse:
    """
    get current user contact
    """
    user: User = await auth_service.get_current_user(request)
    contact: ContactDTO = await contact_service.get_contact_by_user_id(user.id)
    if not contact:
        return JSONResponse(content={"error": "contact not found"}, status_code=404)
    return ContactResponse(
        phone_number=contact.phone_number,
        github_url=contact.github_url,
        linkedin_url=contact.linkedin_url,
        website_url=contact.website_url
    )
