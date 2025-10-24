from sqlalchemy import select
from app.profile.models.contact import Contact
from sqlalchemy.ext.asyncio import AsyncSession


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_contact_by_user_id(self, user_id: int) -> Contact | None:
        """
        get contact by user id
        args:
            user_id: int
        """ 
        try:
            stmt = select(Contact).where(Contact.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e