from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from app.auth.models import *
from app.core.settings import SETTINGS



async def delete_refresh_token_from_db(refresh_token: str, db: AsyncSession):
    """
    delete refresh token from db
    """
    stmt = delete(RefreshToken).where(RefreshToken.token == refresh_token)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def create_refresh_token_to_db(refresh_token: str, user_id: int, db: AsyncSession):
    """
    create refresh token db
    """
    stmt = insert(RefreshToken).values(
            token=refresh_token,
            user_id=user_id,
            expires_at=datetime.datetime.utcnow() +
            datetime.timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES)
        ).returning(RefreshToken)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def get_user_by_email(email, db: AsyncSession):
    """
    get user by email
    args:
        email: str
    """
    stmt = select(User).where(User.email == email)
    user = await db.execute(stmt)
    return user.scalar_one_or_none()


async def create_auth_user(data, db: AsyncSession):
    """
    create user by social
    args:
        data: dict
    """
    stmt = insert(User).values(
            email=data['email'],
            passport_certi=False
        ).returning(User)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()

