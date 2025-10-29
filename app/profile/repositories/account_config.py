from sqlalchemy import select, insert, update
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
        
    async def create_account_config(self, user_id: int, account_config_data: dict) -> AccountConfig:
        """
        create account config
        args:
            user_id: int
            account_config_data: dict
        """
        try:
            stmt = insert(AccountConfig).values(
                user_id=user_id,
                sns_message_notice=account_config_data['sns_message_notice'],
                email_notice=account_config_data['email_notice']
            ).returning(AccountConfig)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except Exception as e:
            raise e
        
    async def update_account_config(self, user_id: int, account_config_data: dict) -> AccountConfig | None:
        """
        update account config
        args:
            user_id: int
            account_config_data: dict
        """
        try:
            stmt = update(AccountConfig).values(account_config_data).where(AccountConfig.user_id == user_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            raise e