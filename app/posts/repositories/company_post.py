from math import e
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.models.company_post import CompanyPost

class CompanyPostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list_company_posts_by_company_id(self, company_id: int) -> list[CompanyPost] | None:
        """
        get list company posts by company id
        args:
            company_id: int
        """
        try:
            stmt = select(CompanyPost).where(CompanyPost.company_id == company_id)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e

    async def get_company_post_by_company_post_id(self, company_post_id: int) -> CompanyPost | None:
        """
        get company post by company post id
        args:
            company_post_id: int
        """
        try:
            stmt = select(CompanyPost).where(CompanyPost.id == company_post_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def create_company_post(self, company_post_data: dict) -> CompanyPost | None:
        """
        create company post
        args:
            company_post_data: dict
        """
        try:
            stmt = insert(CompanyPost).values(company_post_data).returning(CompanyPost)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def update_company_post(self, company_post_data: dict) -> CompanyPost | None:
        """
        update company post
        args:
            company_post_data: dict
        """
        try:
            stmt = update(CompanyPost).values(company_post_data).where(CompanyPost.id == company_post_data['id']).returning(CompanyPost)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def delete_company_post(self, company_post: CompanyPost) -> bool:
        """
        delete company post
        args:
            company_post: CompanyPost
        """
        try:
            await self.session.delete(company_post)
            await self.session.commit()
            return True
        except Exception as e:
            raise e