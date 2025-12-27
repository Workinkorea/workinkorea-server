from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.repositories.company_post import CompanyPostRepository
from app.posts.models.company_post import CompanyPost
from app.posts.schemas.company_post import CompanyPostDTO

from app.posts.schemas.response import CompanyPostResponse

class CompanyPostService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_post_repository = CompanyPostRepository(session)

    async def get_list_company_posts_by_company_id(self, company_id: int) -> list[CompanyPost] | None:
        """
        get company post by company id
        args:
            company_id: int
        """
        company_posts = await self.company_post_repository.get_list_company_posts_by_company_id(company_id)
        if not company_posts:
            raise ValueError("Company post not found")
        return [CompanyPostDTO.model_validate(post).model_dump(mode="json") for post in company_posts]

    async def get_company_post_by_company_post_id(self, company_post_id: int) -> CompanyPostDTO | None:
        """
        get company post by company post id
        args:
            company_post_id: int
        """
        company_post = await self.company_post_repository.get_company_post_by_company_post_id(company_post_id)
        if not company_post:
            raise ValueError("Company post not found")
        return CompanyPostDTO.model_validate(company_post)

    async def create_company_post(self, company_post_data: dict) -> CompanyPostDTO | None:
        """
        create company post
        args:
            company_post_data: dict
        """
        company_post = await self.company_post_repository.create_company_post(company_post_data)
        if not company_post:
            raise ValueError("Failed to create company post")
        return CompanyPostDTO.model_validate(company_post)

    async def update_company_post(self, company_post_data: dict) -> CompanyPostDTO | None:
        """
        update company post
        args:
            company_post_data: dict
        """
        company_post = await self.company_post_repository.get_company_post_by_company_post_id(company_post_data['id'])
        if not company_post:
            raise ValueError("Company post not found")

        if company_post.title == company_post_data['title'] and  \
            company_post.content == company_post_data['content'] and \
            company_post.work_experience == company_post_data['work_experience'] and \
            company_post.position_id == company_post_data['position_id'] and \
            company_post.education == company_post_data['education'] and \
            company_post.language == company_post_data['language'] and \
            company_post.employment_type == company_post_data['employment_type'] and \
            company_post.work_location == company_post_data['work_location'] and \
            company_post.working_hours == company_post_data['working_hours'] and \
            company_post.salary == company_post_data['salary'] and \
            company_post.start_date == company_post_data['start_date'] and \
            company_post.end_date == company_post_data['end_date']:
            raise ValueError("Company post is the same")

        company_post = await self.company_post_repository.update_company_post(company_post_data)
        if not company_post:
            raise ValueError("Failed to update company post")
        return CompanyPostDTO.model_validate(company_post)

    async def delete_company_post(self, company_post_id: int, company_id: int) -> bool:
        """
        delete company post
        args:
            company_post_id: int
        """

        company_post = await self.company_post_repository.get_company_post_by_company_post_id(company_post_id)
        if not company_post:
            raise ValueError("Company post not found")

        if company_post.company_id != company_id:
            raise ValueError("You are not authorized to delete this company post")

        return await self.company_post_repository.delete_company_post(company_post_id)

    async def get_list_company_posts(self, skip: int = 0, limit: int = 100) -> list[CompanyPostDTO] | None:
        """
        get list company posts
        args:
            skip: int
            limit: int
        """
        company_posts = await self.company_post_repository.get_company_posts(skip, limit)
        if not company_posts:
            return []
        return [CompanyPostDTO.model_validate(post).model_dump(mode="json") for post in company_posts]