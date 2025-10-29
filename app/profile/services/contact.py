from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.schemas.contact import ContactDTO
from app.profile.repositories.contact import ContactRepository


class ContactService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.contact_repository = ContactRepository(session)

    async def get_contact_by_user_id(self, user_id: int) -> ContactDTO | None:
        """
        get contact by user id
        args:
            user_id: int
        """
        contact = await self.contact_repository.get_contact_by_user_id(user_id)
        if not contact:
            return None
        return ContactDTO.model_validate(contact)

    async def update_contact(self, user_id: int, contact_data: dict) -> ContactDTO | None:
        """
        update contact
        args:
            user_id: int
            contact_data: dict
        """
        updated_contact = await self.contact_repository.update_contact(user_id, contact_data)
        if not updated_contact:
            return None
        return ContactDTO.model_validate(updated_contact)