from sqlalchemy.ext.asyncio import AsyncSession
from app.admin.repositories.notice import AdminNoticeRepository
from app.admin.schemas.notice import NoticeResponse


class AdminNoticeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.notice_repository = AdminNoticeRepository(session)

    async def create_notice(self, notice_data: dict, author_id: int) -> NoticeResponse:
        """
        공지 생성
        """
        notice_data["author_id"] = author_id
        notice = await self.notice_repository.create_notice(notice_data)
        return NoticeResponse.model_validate(notice)

    async def get_all_notices(self, skip: int = 0, limit: int = 100) -> list[NoticeResponse]:
        """
        공지 가져오기
        """
        notices = await self.notice_repository.get_all_notices(skip, limit)
        return [NoticeResponse.model_validate(notice) for notice in notices]

    async def get_notice_by_title(self, title: str) -> list[NoticeResponse]:
        """
        공지 제목으로 검색
        """
        notices = await self.notice_repository.get_notice_by_title(title)
        return [NoticeResponse.model_validate(notice) for notice in notices]

    async def get_notice_by_id(self, notice_id: int) -> NoticeResponse:
        """
        공지 아이디로 하나만 가져오기
        """
        notice = await self.notice_repository.get_notice_by_id(notice_id)
        if not notice:
            raise ValueError("Notice not found")
        return NoticeResponse.model_validate(notice)

    async def update_notice(self, notice_id: int, notice_data: dict) -> NoticeResponse:
        """
        공지 수정
        """
        existing_notice = await self.notice_repository.get_notice_by_id(notice_id)
        if not existing_notice:
            raise ValueError("Notice not found")
        
        updated_notice = await self.notice_repository.update_notice(notice_id, notice_data)
        return NoticeResponse.model_validate(updated_notice)

    async def delete_notice(self, notice_id: int) -> bool:
        """
        공지 삭제
        """
        notice = await self.notice_repository.get_notice_by_id(notice_id)
        if not notice:
            raise ValueError("Notice not found")
        
        return await self.notice_repository.delete_notice(notice)
