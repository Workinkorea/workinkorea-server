from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.models.profile import Profile


class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
 
    async def create_profile(self, user_data: dict) -> Profile | None:
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
            await self.session.commit()
            return result.scalar_one_or_none()
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
        
    async def update_profile(self, user_id: int, profile_data: dict) -> bool:
        """
        update profile
        args:
            user_id: int
            profile_data: dict
        """
        try:
            stmt = update(Profile).values(profile_data).where(Profile.user_id == user_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except Exception as e:
            raise e
        
    async def delete_profile(self, user_id: int) -> bool:
        """
        delete profile
        args:
            user_id: int
        """
        try:
            stmt = delete(Profile).where(Profile.user_id == user_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except Exception as e:
            raise e
