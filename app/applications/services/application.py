from sqlalchemy.ext.asyncio import AsyncSession
from app.applications.repositories.application import ApplicationRepository
from app.applications.schemas.application import ApplicationDTO, ApplicantResponse
from app.posts.repositories.company_post import CompanyPostRepository


class ApplicationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.application_repository = ApplicationRepository(session)
        self.company_post_repository = CompanyPostRepository(session)

    async def create_application(self, user_id: int, company_post_id: int) -> ApplicationDTO:
        company_post = await self.company_post_repository.get_company_post_by_company_post_id(company_post_id)
        if not company_post:
            raise ValueError("Company post not found")

        existing = await self.application_repository.get_application_by_user_and_post(user_id, company_post_id)
        if existing:
            raise ValueError("Already applied to this post")

        application = await self.application_repository.create_application({
            "user_id": user_id,
            "company_post_id": company_post_id,
            "status": "pending",
        })
        if not application:
            raise ValueError("Failed to create application")
        return ApplicationDTO.model_validate(application)

    async def get_my_applications(self, user_id: int) -> list[ApplicationDTO]:
        applications = await self.application_repository.get_applications_by_user_id(user_id)
        return [ApplicationDTO.model_validate(a) for a in applications]

    async def cancel_application(self, application_id: int, user_id: int) -> bool:
        application = await self.application_repository.get_application_by_id(application_id)
        if not application:
            raise ValueError("Application not found")
        if application.user_id != user_id:
            raise PermissionError("Not authorized to cancel this application")
        return await self.application_repository.delete_application(application)

    async def get_applicants_by_post(self, company_post_id: int, company_id: int) -> list[ApplicantResponse]:
        company_post = await self.company_post_repository.get_company_post_by_company_post_id(company_post_id)
        if not company_post:
            raise ValueError("Company post not found")
        if company_post.company_id != company_id:
            raise PermissionError("Not authorized to view applicants for this post")

        applications = await self.application_repository.get_applications_by_company_post_id(company_post_id)
        return [ApplicantResponse.model_validate(a) for a in applications]
