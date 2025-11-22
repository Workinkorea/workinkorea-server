from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.repositories.resume import ResumeRepository
from app.posts.schemas.resume import (
    LanguageSkillsDTO, 
    SchoolsDTO,
    CareerHistoryDTO, 
    IntroductionDTO, 
    LicensesDTO, 
    ResumeListDTO
)


from app.posts.models.resume import Resume

class ResumeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.resume_repository = ResumeRepository(session)

    async def get_resume_list_by_user_id(self, user_id: int) -> list[Resume] | None:
        """
        get resume list by user id
        args:
            user_id: int
        """
        resume_list = await self.resume_repository.get_resume_list_by_user_id(user_id)
        if not resume_list:
            raise ValueError("Resume list not found")
        return [ResumeListDTO.model_validate(resume).model_dump(mode="json") for resume in resume_list]
       

    async def get_resume_by_resume_id(self, resume_id: int, user_id: int) -> Resume | None:
        """
        get resume by user id
        args:
            user_id: int
        """
        resume_data = await self.resume_repository.get_resume_by_resume_id(resume_id)
        if not resume_data:
            raise ValueError("Resume not found")
        
        if resume_data.user_id != user_id:
            raise ValueError("You are not authorized to view this resume")

        language_skills = [LanguageSkillsDTO.model_validate(language_skill).model_dump(mode="json") for language_skill in resume_data.language_skills]
        schools = [SchoolsDTO.model_validate(school).model_dump(mode="json") for school in resume_data.schools]
        career_history = [CareerHistoryDTO.model_validate(career_history).model_dump(mode="json") for career_history in resume_data.career_history]
        introduction = [IntroductionDTO.model_validate(introduction).model_dump(mode="json") for introduction in resume_data.introduction]
        licenses = [LicensesDTO.model_validate(license).model_dump(mode="json") for license in resume_data.licenses]

        resume ={
            "id": resume_data.id,
            "user_id": resume_data.user_id,
            "title": resume_data.title,
            "profile_url": resume_data.profile_url,
            "language_skills": language_skills,
            "schools": schools,
            "career_history": career_history,
            "introduction": introduction,
            "licenses": licenses,
        }
        return resume
        
        
    async def create_resume(self, resume_data: dict) -> Resume | None:
        """
        create resume
        args:
            resume_data: dict
        """
        resume_id = await self.resume_repository.create_resume_with_relations(resume_data)
        if not resume_id:
            raise ValueError("Failed to create resume")
        
        return resume_id
        

    async def update_resume(self, resume_data: dict, user_id: int) -> Resume | None:
        """
        update resume
        args:
            resume_id: int
            resume_data: dict
        """
        resume = await self.resume_repository.get_resume_by_resume_id(resume_data['id'])
        if not resume:
            raise ValueError("Resume not found")
        
        if resume.user_id != user_id:
            raise ValueError("You are not authorized to update this resume")
        
        # 업데이트할 내용이 없으면 예외 발생
        if resume.title == resume_data['title'] and \
            resume.profile_url == resume_data['profile_url'] and \
            resume.language_skills == resume_data['language_skills'] and \
            resume.schools == resume_data['schools'] and \
            resume.career_history == resume_data['career_history'] and \
            resume.introduction == resume_data['introduction'] and \
            resume.licenses == resume_data['licenses']:
            raise ValueError("Resume is the same")
        
        resume_id = await self.resume_repository.update_resume_with_relations( resume, resume_data)
        if not resume_id:
            raise ValueError("Failed to update resume")
        return resume_id
        
        
    
    async def delete_resume(self, resume_id: int, user_id: int) -> bool:
        """
        delete resume
        args:
            resume_id: int
        """
        resume = await self.resume_repository.get_resume_by_resume_id(resume_id)
        if not resume:
            raise ValueError("Resume not found")
        
        if resume.user_id != user_id:
            raise ValueError("You are not authorized to delete this resume")

        return await self.resume_repository.delete_resume(resume)