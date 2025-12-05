from sqlalchemy.ext.asyncio import AsyncSession
from app.admin.repositories.company_post import AdminCompanyPostRepository
from app.admin.schemas.company_post import CompanyPostResponse


class AdminCompanyPostService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_post_repository = AdminCompanyPostRepository(session)

    async def get_all_company_posts(self, skip: int = 0, limit: int = 100) -> list[CompanyPostResponse]:
        """
        Get all company posts with pagination
        """
        posts = await self.company_post_repository.get_all_company_posts(skip, limit)
        return [CompanyPostResponse.model_validate(post) for post in posts]

    async def get_company_post_by_id(self, post_id: int) -> CompanyPostResponse | None:
        """
        Get company post by id
        """
        post = await self.company_post_repository.get_company_post_by_id(post_id)
        if not post:
            raise ValueError("Company post not found")
        return CompanyPostResponse.model_validate(post)

    async def update_company_post(self, post_id: int, post_data: dict) -> CompanyPostResponse:
        """
        Update company post
        """
        existing_post = await self.company_post_repository.get_company_post_by_id(post_id)
        if not existing_post:
            raise ValueError("Company post not found")

        updated_post = await self.company_post_repository.update_company_post(post_id, post_data)
        if not updated_post:
            raise ValueError("Failed to update company post")
        return CompanyPostResponse.model_validate(updated_post)

    async def delete_company_post(self, post_id: int) -> bool:
        """
        Delete company post
        """
        post = await self.company_post_repository.get_company_post_by_id(post_id)
        if not post:
            raise ValueError("Company post not found")

        return await self.company_post_repository.delete_company_post(post)
