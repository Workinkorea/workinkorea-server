from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.auth.models import User


"""
모델들은 걍 기존에 있던거 쓰면 되서 굳이 안만들었음
"""


class AdminUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        유저 목록 페이지네이션으로 가져옴
        args:
            skip: int
            limit: int
        returns:
            list[User]
        raises:
            Exception
        """
        try:
            stmt = select(User).options(selectinload(User.profile)).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        유저 아이디로 하나만 가져옴
        args:
            user_id: int
        returns:
            User | None
        raises:
            Exception
        """
        try:
            stmt = select(User).options(selectinload(User.profile)).where(User.id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def update_user(self, user_id: int, user_data: dict) -> User | None:
        """
        유저 수정하기
        args:
            user_id: int
            user_data: dict
        returns:
            User | None
        raises:
            Exception
        """
        try:
            stmt = update(User).where(User.id == user_id).values(user_data).returning(User)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e

    async def delete_user(self, user: User) -> bool:
        """
        유저 삭제하기
        args:
            user: User
        returns:
            bool
        raises:
            Exception
        """
        try:
            await self.session.delete(user)
            await self.session.commit()
            return True
        except Exception as e:
            raise e
