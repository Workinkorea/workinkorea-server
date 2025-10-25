from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.models.account_config import AccountConfig


class AccountConfigRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_account_config_by_user_id(self, user_id: int) -> AccountConfig | None:
        """
        get account config by user id
        args:
            user_id: int
        """
        try:
            stmt = select(AccountConfig).where(AccountConfig.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e