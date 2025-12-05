from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.models.position import Position


class PositionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_position_by_position_id(self, position_id: int) -> Position | None:
        """
        get position by position id
        args:
            position_id: int
        """
        try:
            stmt = select(Position).where(Position.id == position_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e