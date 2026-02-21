from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.dependencies import get_admin_user
from app.admin.schemas.email import BulkEmailSendRequest, BulkEmailSendResponse
from app.admin.services.email import EmailService
from app.auth.models import User
from app.database import get_async_session


router = APIRouter(
    prefix="/emails",
    tags=["emails"]
)


def get_email_service(session: AsyncSession = Depends(get_async_session)):
    return EmailService(session)


@router.post("/bulk", response_model=BulkEmailSendResponse)
async def send_bulk_email(
    payload: BulkEmailSendRequest,
    admin_user: User = Depends(get_admin_user),
    email_service: EmailService = Depends(get_email_service),
):
    """
    단체 이메일 발송 기능 (email_notice=True 수신 동의 유저 대상)
    """
    try:
        sent_count = await email_service.send_bulk_email_to_opted_users(
            subject=payload.subject,
            title=payload.title,
            content=payload.content,
        )
        return BulkEmailSendResponse(
            message="Bulk email sent successfully",
            sent_count=sent_count,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
