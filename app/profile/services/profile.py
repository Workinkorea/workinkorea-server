from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.schemas.profile import ProfileDTO
from app.profile.repositories.profile import ProfileRepository


class ProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profile_repository = ProfileRepository(session)

    async def get_profile_by_user_id(self, user_id: int) -> ProfileDTO | None:
        """
        get profile by user id
        args:
            user_id: int
        """
        profile = await self.profile_repository.get_profile_by_user_id(user_id)
        if not profile:
            return None
        return ProfileDTO.model_validate(profile)

    async def create_profile(self, user_data: dict) -> bool:
        """
        create profile
        args:
            user_data: dict
        """
        created = await self.profile_repository.create_profile(user_data)
        if not created:
            return False
        return True

    async def update_profile(self, user_id: int, profile_data: dict) -> bool:
        """
        update profile
        args:
            user_id: int
            profile_data: dict
        """
        profile = await self.profile_repository.get_profile_by_user_id(user_id)
        if not profile:
            return False
        updated = await self.profile_repository.update_profile(user_id, profile_data)
        if not updated:
            return False
        return True

    async def delete_profile(self, user_id: int) -> bool:
        """
        delete profile
        args:
            user_id: int
        """
        deleted = await self.profile_repository.delete_profile(user_id)
        if not deleted:
            return False
        return True
