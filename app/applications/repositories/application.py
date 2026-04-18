from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.applications.models.application import Application


class ApplicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_application(self, data: dict) -> Application:
        try:
            stmt = insert(Application).values(data).returning(Application)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def get_application_by_id(self, id: int) -> Application | None:
        try:
            stmt = select(Application).where(Application.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def get_application_by_user_and_post(self, user_id: int, company_post_id: int) -> Application | None:
        try:
            stmt = select(Application).where(
                Application.user_id == user_id,
                Application.company_post_id == company_post_id
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def get_applications_by_user_id(self, user_id: int) -> list[Application]:
        try:
            stmt = select(Application).where(Application.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e

    async def get_applications_by_company_post_id(self, company_post_id: int) -> list[Application]:
        try:
            stmt = select(Application).where(Application.company_post_id == company_post_id)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e

    async def delete_application(self, application: Application) -> bool:
        try:
            await self.session.delete(application)
            await self.session.commit()
            return True
        except Exception as e:
            raise e
