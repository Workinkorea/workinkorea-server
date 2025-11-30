from sqlalchemy.ext.asyncio import AsyncSession
from app.admin.repositories.user import AdminUserRepository
from app.admin.schemas.user import UserResponse


class AdminUserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = AdminUserRepository(session)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        """
        Get all users with pagination
        """
        users = await self.user_repository.get_all_users(skip, limit)
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse | None:
        """
        Get user by id
        """
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_data: dict) -> UserResponse:
        """
        Update user
        """
        existing_user = await self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            raise ValueError("User not found")

        updated_user = await self.user_repository.update_user(user_id, user_data)
        if not updated_user:
            raise ValueError("Failed to update user")
        return UserResponse.model_validate(updated_user)

    async def delete_user(self, user_id: int) -> bool:
        """
        Delete user
        """
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return await self.user_repository.delete_user(user)
