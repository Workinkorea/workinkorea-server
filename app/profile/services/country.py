from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.schemas.country import CountryDTO
from app.profile.repositories.country import CountryRepository


class CountryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.country_repository = CountryRepository(session)

    async def get_country_by_country_code(self, country_code: str) -> CountryDTO | None:
        """
        get country by country code
        args:
            country_code: str
        """
        country = await self.country_repository.get_country_by_country_code(country_code)
        if not country:
            return None
        return CountryDTO.model_validate(country)