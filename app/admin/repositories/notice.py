from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.admin.models import Notice

class AdminNoticeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_notice(self, notice_data: dict) -> Notice:
        """
        공지 생성
        """
        notice = Notice(**notice_data)
        self.session.add(notice)
        await self.session.commit()
        await self.session.refresh(notice)
        return notice

    async def get_all_notices(self, skip: int = 0, limit: int = 100) -> list[Notice]:
        """
        모든 공지 가져오기
        """
        stmt = select(Notice).offset(skip).limit(limit).order_by(Notice.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_notice_by_id(self, notice_id: int) -> Notice | None:
        """
        단일 공지 아이디로 가져오기
        """
        stmt = select(Notice).where(Notice.id == notice_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_notice_by_title(self, title: str) -> list[Notice]:
        """
        공지 제목(포함 검색)으로 가져오기
        """
        stmt = select(Notice).where(Notice.title.like(f"%{title}%"))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_notice(self, notice_id: int, notice_data: dict) -> Notice | None:
        """
        공지 업데이트
        """
        stmt = update(Notice).where(Notice.id == notice_id).values(**notice_data).returning(Notice)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete_notice(self, notice: Notice) -> bool:
        """
        공지 찾기
        """
        await self.session.delete(notice)
        await self.session.commit()
        return True
