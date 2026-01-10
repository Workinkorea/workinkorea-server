from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.admin.dependencies import get_admin_user
from app.admin.services.notice import AdminNoticeService
from app.admin.schemas.notice import NoticeCreate, NoticeUpdate, NoticeResponse
from app.auth.models import User


router = APIRouter(
    prefix="/notices",
    tags=["admin-notices"]
)


def get_admin_notice_service(session: AsyncSession = Depends(get_async_session)):
    return AdminNoticeService(session)


@router.post("/", response_model=NoticeResponse)
async def create_notice(
    payload: NoticeCreate,
    admin_user: User = Depends(get_admin_user),
    notice_service: AdminNoticeService = Depends(get_admin_notice_service)
):
    """
    공지사항 작성
    """
    try:
        notice_data = payload.model_dump()
        # 이메일 전송 여기 넣어야 할 수 있음
        notice = await notice_service.create_notice(notice_data, admin_user.id)
        return notice
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/", response_model=list[NoticeResponse])
async def get_all_notices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin_user: User = Depends(get_admin_user),
    notice_service: AdminNoticeService = Depends(get_admin_notice_service)
):
    """
    공지사항 목록 조회
    """
    try:
        notices = await notice_service.get_all_notices(skip, limit)
        return notices
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/search", response_model=list[NoticeResponse])
async def get_notice_by_title(
    title: str = Query(..., min_length=1),
    admin_user: User = Depends(get_admin_user),
    notice_service: AdminNoticeService = Depends(get_admin_notice_service)
):
    """
    공지사항 제목 검색
    """
    try:
        notices = await notice_service.get_notice_by_title(title)
        return notices
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice_by_id(
    notice_id: int,
    admin_user: User = Depends(get_admin_user),
    notice_service: AdminNoticeService = Depends(get_admin_notice_service)
):
    """
    특정 공지사항 조회
    """
    try:
        notice = await notice_service.get_notice_by_id(notice_id)
        return notice
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.patch("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: int,
    payload: NoticeUpdate,
    admin_user: User = Depends(get_admin_user),
    notice_service: AdminNoticeService = Depends(get_admin_notice_service)
):
    """
    공지 수정
    """
    try:
        notice_data = payload.model_dump(exclude_unset=True)
        updated_notice = await notice_service.update_notice(notice_id, notice_data)
        return updated_notice
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/{notice_id}")
async def delete_notice(
    notice_id: int,
    admin_user: User = Depends(get_admin_user),
    notice_service: AdminNoticeService = Depends(get_admin_notice_service)
):
    """
    공지사항 삭제
    """
    try:
        deleted = await notice_service.delete_notice(notice_id)
        if not deleted:
            raise ValueError("Failed to delete notice")
        return JSONResponse(content={"message": "Notice deleted successfully"}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
