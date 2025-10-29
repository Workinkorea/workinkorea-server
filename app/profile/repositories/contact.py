from sqlalchemy import select, insert, update
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

    async def create_contact(self, user_id: int, contact_data: dict) -> Contact:
        """
        create contact
        args:
            user_id: int
            contact_data: dict
        """
        try:
            stmt = insert(Contact).values(user_id=user_id, **contact_data).returning(Contact)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except Exception as e:
            raise e
        
    async def update_contact(self, user_id: int, contact_data: dict) -> Contact | None:
        """
        update contact
        args:
            user_id: int
            contact_data: dict
        """
        try:
            stmt = update(Contact).values(contact_data).where(Contact.user_id == user_id).returning(Contact)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e