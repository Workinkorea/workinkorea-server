from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.schemas.account_config import AccountConfigDTO
from app.profile.repositories.account_config import AccountConfigRepository


class AccountConfigService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.account_config_repository = AccountConfigRepository(session)

    async def get_account_config_by_user_id(self, user_id: int) -> AccountConfigDTO | None:
        """
        get account config by user id
        args:
            user_id: int
        """
        account_config = await self.account_config_repository.get_account_config_by_user_id(user_id)
        if not account_config:
            return None
        return AccountConfigDTO.model_validate(account_config)

    async def create_account_config(self, user_id: int) -> AccountConfigDTO | None:
        """
        create account config with default values
        args:
            user_id: int
        """
        account_config = await self.account_config_repository.create_account_config(user_id, {
            'sns_message_notice': True,
            'email_notice': True,
        })
        if not account_config:
            return None
        return AccountConfigDTO.model_validate(account_config)

    async def update_account_config(self, user_id: int, account_config_data: dict) -> bool:
        """
        update account config to db
        args:
            user_id: int
            account_config_data: dict 
        """
        updated = await self.account_config_repository.update_account_config(user_id, account_config_data)
        if not updated:
            return None
        return AccountConfigDTO.model_validate(updated)