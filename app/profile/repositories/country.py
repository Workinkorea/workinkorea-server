from sqlalchemy import select
from app.profile.models.country import Country
from sqlalchemy.ext.asyncio import AsyncSession


class CountryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_country_by_country_code(self, country_code: str) -> Country | None:
        """
        get country by country code
        args:
            country_code: str
        """
        try:
            stmt = select(Country).where(Country.code == country_code)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise e