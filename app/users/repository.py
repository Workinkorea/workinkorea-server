from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import *


class UsersRepository:
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
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def create_profile(self, user_data: dict) -> Profile:
        """
        create basic profile
        args:
            user_data: dict
        """
        try:
            stmt = insert(Profile).values(
                user_id=user_data['user_id'],
                name=user_data['name'],
                birth_date=user_data['birth_date'],
                country_id=user_data['country_id'],
            ).returning(Profile)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except Exception as e:
            raise e

    async def get_profile_by_user_id(self, user_id: int) -> Profile | None:
        """
        get profile by user id
        args:
            user_id: int
        """
        try:
            stmt = select(Profile).where(Profile.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def update_profile(self, profile_id: int, data: dict) -> bool:
        """
        update profile
        args:
            profile_id: int
            data: dict
        """
        try:
            stmt = update(Profile).values(data).where(Profile.id == profile_id)
            await self.session.execute(stmt)
            return True
        except Exception as e:
            raise e

    async def delete_profile(self, profile_id: int) -> bool:
        """
        delete profile
        """
        try:
            stmt = delete(Profile).where(Profile.id == profile_id)
            await self.session.execute(stmt)
            return True
        except Exception as e:
            raise e

    async def get_country_code(self, country_code: str) -> Country | None:
        """
        get country by code
        args:
            country_code: str
        """
        try:
            stmt = select(Country).where(Country.code == country_code)
            result = await self.session.execute(stmt)
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
            # selectinload: 즉시 로딩
            from sqlalchemy.orm import selectinload 
            stmt = select(User).options(selectinload(User.profile)).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e
