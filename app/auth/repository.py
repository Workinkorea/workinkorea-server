from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from app.auth.models import *
from app.core.settings import SETTINGS


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_refresh_token_from_db(self, refresh_token: str) -> bool:
        """
        delete refresh token from db
        args:
            refresh_token: str
        """
        try:
            stmt = delete(RefreshToken).where(RefreshToken.token == refresh_token)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except Exception as e:
            raise e

    async def create_refresh_token_to_db(self, refresh_token: str, user_id: int) -> RefreshToken | None:
        """
        create refresh token db
        args:
            refresh_token: str
            user_id: int
        """
        try:
            stmt = insert(RefreshToken).values(
                token=refresh_token,
                user_id=user_id,
                expires_at=datetime.datetime.utcnow() +
                datetime.timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES)
            ).returning(RefreshToken)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

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
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e