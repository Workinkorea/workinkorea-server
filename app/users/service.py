# app/users/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.repository import UsersRepository
from app.users.models import Profile, User, Country
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from app.core.settings import SETTINGS

class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users_repository = UsersRepository(session)

    async def get_profile_by_user_id(self, user_id: int) -> Profile | None:
        """
        get profile by user id
        args:
            user_id: int
        """
        return await self.users_repository.get_profile_by_user_id(user_id)

    async def get_current_user(request: Request):
        """
        get current user
        """
        access_token = request.cookies.get("access_token")

        if not access_token:
            return JSONResponse(content={"message": "Not authenticated"}, status_code=401)

        try:
            # jwt token 검증 이메일 반환
            payload = jwt.decode(access_token, SETTINGS.JWT_SECRET,
                                algorithms=[SETTINGS.JWT_ALGORITHM])

            email = payload.get("sub")
            if not email:
                return JSONResponse(content={"message": "Invalid token"}, status_code=401)
            return email
        except jwt.ExpiredSignatureError:
            return JSONResponse(content={"message": "Access token expired"}, status_code=401)
        except Exception as e:
            return JSONResponse(content={"message": "Invalid token"}, status_code=401)

    async def create_user_by_social(self, user_info_data: dict) -> tuple[User, Profile] | JSONResponse:
        """
        create user by social
        args:
            user_info_data: dict
        """
        user = await self.users_repository.create_user_by_social(user_info_data)
        if not user:
            return JSONResponse(content={"error": "failed to create user"}, status_code=500)
        
        user_info_data['user_id'] = user.id
        profile = await self.users_repository.create_profile(user_info_data)
        if not profile:
            return JSONResponse(content={"error": "failed to create profile"}, status_code=500)
        
        return user, profile

    async def update_profile(self, user_id: int, data: dict) -> bool:
        """
        update profile
        args:
            user_id: int
            data: dict
        """
        profile = await self.users_repository.get_profile_by_user_id(user_id)
        if not profile:
            return JSONResponse(content={"error": "profile not found"}, status_code=404)
        return await self.users_repository.update_profile(profile.id, data)

    async def delete_profile(self, profile_id: int) -> bool:
        """
        delete profile
        args:
            profile_id: int
        """
        return await self.users_repository.delete_profile(profile_id)

    async def get_country_code(self, country_code: str) -> Country | None:
        """
        get country by code
        args:
            country_code: str
        """
        return await self.users_repository.get_country_code(country_code)

    async def get_user_by_email(self, email: str) -> User | None:
        """
        get user by email
        args:
            email: str
        """
        return await self.users_repository.get_user_by_email(email)
