from sqlalchemy import select, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from sqlalchemy.orm import selectinload

from app.auth.models import User
from app.core.settings import SETTINGS


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_by_social(self, data: dict) -> User | None:
        """
        create user
        args:
            data: dict
        """
        try:
            stmt = insert(User).values(
                email=data['email'],
                passport_certi=False
            ).returning(User)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def get_user_by_email(self, email: str) -> User | None:
        """
        get user by email
        args:
            email: str
        """
        try:
            stmt = select(User).options(selectinload(User.profile)).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e
    
    async def update_user_company_info(self, email: str, company_info: dict) -> User | None:
        """
        update company user
        args:
            user_id: int
            company_info: dict
        """
        try:
            stmt = update(User).values(company_info=company_info).where(User.email == email).returning(User)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e