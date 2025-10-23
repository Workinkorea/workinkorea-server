# app/profile/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.repository import ProfileRepository
from app.profile.models import Profile, Country
from app.auth.models import User
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from app.core.settings import SETTINGS

class ProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profile_repository = ProfileRepository(session)

    async def get_profile_by_user_id(self, user_id: int) -> Profile | None:
        """
        get profile by user id
        args:
            user_id: int
        """
        return await self.profile_repository.get_profile_by_user_id(user_id)

    async def update_profile(self, user_id: int, data: dict) -> bool:
        """
        update profile
        args:
            user_id: int
            data: dict
        """
        profile = await self.profile_repository.get_profile_by_user_id(user_id)
        if not profile:
            return JSONResponse(content={"error": "profile not found"}, status_code=404)
        return await self.profile_repository.update_profile(profile.id, data)

    async def delete_profile(self, profile_id: int) -> bool:
        """
        delete profile
        args:
            profile_id: int
        """
        return await self.profile_repository.delete_profile(profile_id)

    async def get_country_code(self, country_code: str) -> Country | None:
        """
        get country by code
        args:
            country_code: str
        """
        return await self.profile_repository.get_country_code(country_code)
