from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.models.company_post import CompanyPost


"""
모델들은 걍 기존에 있던거 쓰면 되서 굳이 안만들었음
"""


class AdminCompanyPostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_company_posts(self, skip: int = 0, limit: int = 100) -> list[CompanyPost]:
        """
        회사 공고 페이지네이션으로 가져옴
        args:
            skip: int
            limit: int
        returns:
            list[CompanyPost]
        raises:
            Exception
        """
        try:
            stmt = select(CompanyPost).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e

    async def get_company_post_by_id(self, post_id: int) -> CompanyPost | None:
        """
        회사 공고 아이디로 하나만 가져옴
        args:
            post_id: int
        returns:
            CompanyPost | None
        raises:
            Exception
        """
        try:
            stmt = select(CompanyPost).where(CompanyPost.id == post_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def update_company_post(self, post_id: int, post_data: dict) -> CompanyPost | None:
        """
        공고 수정하기
        args:
            post_id: int
            post_data: dict
        returns:
            CompanyPost | None
        raises:
            Exception
        """
        try:
            stmt = update(CompanyPost).where(CompanyPost.id == post_id).values(post_data).returning(CompanyPost)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def delete_company_post(self, company_post: CompanyPost) -> bool:
        """
        공고 삭제하기
        args:
            company_post: CompanyPost
        returns:
            bool
        raises:
            Exception
        """
        try:
            await self.session.delete(company_post)
            await self.session.commit()
            return True
        except Exception as e:
            raise e
