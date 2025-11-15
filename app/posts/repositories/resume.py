from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.models.resume import Resume
from app.posts.models.language_skill import LanguageSkills
from app.posts.models.school import Schools
from app.posts.models.career_history import CareerHistory
from app.posts.models.introduction import Introduction
from app.posts.models.license import Licenses

class ResumeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_resume_list_by_user_id(self, user_id: int) -> Resume | None:
        """
        get resume by user id
        args:
            user_id: int
        """
        try:
            stmt = select(Resume).where(Resume.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e

    async def get_resume_by_resume_id(self, resume_id: int) -> Resume | None:
        """
        get resume by resume id
        args:
            resume_id: int
        """
        try:
            stmt = select(Resume).where(Resume.id == resume_id).options( \
                joinedload(Resume.language_skills), \
                joinedload(Resume.schools), \
                joinedload(Resume.career_history), \
                joinedload(Resume.introduction), \
                joinedload(Resume.licenses) \
            )
            result = await self.session.execute(stmt)
            return result.unique().scalar_one_or_none()
        except Exception as e:
            raise e

    async def create_resume_with_relations(self, resume_data: dict) -> Resume | None:
        """
        create resume with all related models in one transaction
        args:
            resume_data: dict containing resume and related data
        """
        try:
            # Resume ORM 객체 생성
            resume = Resume(
                user_id=resume_data['user_id'],
                title=resume_data['title'],
                profile_url=resume_data['profile_url']
            )
            
            # 관계된 객체들을 생성하고 연결
            if resume_data['language_skills']:
                resume.language_skills = [
                    LanguageSkills(
                        language_type=data['language_type'],
                        level=data['level']
                    ) 
                    for data in resume_data['language_skills']
                ]
            
            if resume_data['schools']:
                resume.schools = [
                    Schools(
                        school_name=data['school_name'],
                        major_name=data['major_name'],
                        start_date=data['start_date'],
                        end_date=data['end_date'],
                        is_graduated=data['is_graduated']
                    )
                    for data in resume_data['schools']
                ]
            
            if resume_data['career_history']:
                resume.career_history = [
                    CareerHistory(
                        company_name=data['company_name'],
                        start_date=data['start_date'],
                        end_date=data['end_date'],
                        is_working=data['is_working'],
                        department=data['department'],
                        position_title=data['position_title'],
                        main_role=data['main_role']
                    )
                    for data in resume_data['career_history']
                ]
            
            if resume_data['introduction']:
                resume.introduction = [
                    Introduction(
                        title=data['title'],
                        content=data['content']
                    )
                    for data in resume_data['introduction']
                ]
            
            if resume_data['licenses']:
                resume.licenses = [
                    Licenses(
                        license_name=data['license_name'],
                        license_agency=data['license_agency'],
                        license_date=data['license_date']
                    )
                    for data in resume_data['licenses']
                ]
            
            # 세션에 추가하고 한 번에 commit
            self.session.add(resume)
            await self.session.flush() 
            await self.session.commit()

            return resume.id
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update_resume_with_relations(self, resume: Resume, resume_data: dict) -> Resume | None:
        """
        update resume
        args:
            resume_data: dict
        """
        try:
            if resume_data['title'] and resume_data['title'] != resume.title:
                resume.title = resume_data['title']

            if resume_data['profile_url'] and resume_data['profile_url'] != resume.profile_url:
                resume.profile_url = resume_data['profile_url']

            if resume_data['language_skills'] and resume_data['language_skills'] != resume.language_skills:

                for skill in list(resume.language_skills):
                    await self.session.delete(skill)
                resume.language_skills.clear()
                # 새로 추가
                resume.language_skills = [
                    LanguageSkills(
                        language_type=data['language_type'],
                        level=data['level']
                    )
                    for data in resume_data['language_skills']
                ]
        
            if resume_data['schools'] and resume_data['schools'] != resume.schools:
                for school in list(resume.schools):
                    await self.session.delete(school)
                resume.schools.clear()
                resume.schools = [
                    Schools(
                        school_name=data['school_name'],
                        major_name=data['major_name'],
                        start_date=data['start_date'],
                        end_date=data['end_date'],
                        is_graduated=data['is_graduated']
                    )
                    for data in resume_data['schools']
                ]
            
            if resume_data['career_history'] and resume_data['career_history'] != resume.career_history:
                for career in list(resume.career_history):
                    await self.session.delete(career)
                resume.career_history.clear()
                resume.career_history = [
                    CareerHistory(
                        company_name=data['company_name'],
                        start_date=data['start_date'],
                        end_date=data['end_date'],
                        is_working=data['is_working'],
                        department=data['department'],
                        position_title=data['position_title'],
                        main_role=data['main_role']
                    )
                    for data in resume_data['career_history']
                ]
            
            if resume_data['introduction'] and resume_data['introduction'] != resume.introduction:
                for intro in list(resume.introduction):
                    await self.session.delete(intro)
                resume.introduction.clear()
                resume.introduction = [
                    Introduction(
                        title=data['title'],
                        content=data['content']
                    )
                    for data in resume_data['introduction']
                ]
            
            if resume_data['licenses'] and resume_data['licenses'] != resume.licenses:
                for license in list(resume.licenses):
                    await self.session.delete(license)
                resume.licenses.clear()
                resume.licenses = [
                    Licenses(
                        license_name=data['license_name'],
                        license_agency=data['license_agency'],
                        license_date=data['license_date']   
                    )
                    for data in resume_data['licenses']
                ]
            
            await self.session.commit()
            return resume.id
        except Exception as e:
            raise e

    
    async def delete_resume(self, resume: Resume) -> bool:
        """
        delete resume
        args:
            resume_id: int
        """
        try:
             await self.session.delete(resume)
             await self.session.commit()
             return True
        except Exception as e:
            raise e