from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.schemas.position import PositionDTO
from app.profile.repositories.position import PositionRepository


class PositionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.position_repository = PositionRepository(session)

    async def get_position_by_position_id(self, position_id: int) -> PositionDTO | None:
        """
        get position by position id
        args:
            position_id: int
        """
        position = await self.position_repository.get_position_by_position_id(position_id)
        if not position:
            return None
        return PositionDTO.model_validate(position)