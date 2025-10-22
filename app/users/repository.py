from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import *

async def get_country_code(country_code: str, db: AsyncSession):
    """
    get country code
    """
    stmt = select(Country).where(Country.code == country_code)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()

async def create_auth_profile(data, db: AsyncSession):
    """
    create auth user
    """
    stmt = insert(Profile).values(
        user_id=data['user_id'],
        name=data['name'],
        birth_date=data['birth_date'],
        country_id=data['country_id'],
    ).returning(Profile)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()