from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from app.auth.models import *
from app.core.settings import SETTINGS

from app.database import redis_client


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_refresh_token_from_db(self, refresh_token: str) -> bool:
        """
        delete refresh token from db
        """
        try:
            stmt = delete(RefreshToken).where(
                RefreshToken.token == refresh_token)
            result = await self.session.execute(stmt)
            return result.rowcount > 0
        except Exception as e:
            raise e

    async def create_refresh_token_to_db(self, refresh_token: str, user_id: int) -> RefreshToken | None:
        """
        create refresh token db
        """
        try:
            stmt = insert(RefreshToken).values(
                token=refresh_token,
                user_id=user_id,
                expires_at=datetime.datetime.utcnow() +
                datetime.timedelta(
                    minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES)
            ).returning(RefreshToken)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

class RedisRepository:
    def __init__(self):
        self.redis = redis_client()

    async def check_redis_ping(self):
        return await self.redis.ping()