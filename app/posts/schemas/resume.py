from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResumeListDTO(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResumeDTO(BaseModel):
    id: int
    user_id: int
    title: str
    profile_url: str = None
    language_skills: Optional[list["LanguageSkillsDTO"]] = None
    schools: Optional[list["SchoolsDTO"]] = None
    career_history: Optional[list["CareerHistoryDTO"]] = None
    introduction: Optional[list["IntroductionDTO"]] = None
    licenses: Optional[list["LicensesDTO"]] = None

    class Config:
        from_attributes = True

class LanguageSkillsDTO(BaseModel):
    language_type: str = None
    level: str = None

    class Config:
        from_attributes = True

class SchoolsDTO(BaseModel):
    school_name: str
    major_name: str
    start_date: datetime
    end_date: datetime = None
    is_graduated: bool

    class Config:
        from_attributes = True

class CareerHistoryDTO(BaseModel):
    company_name: str
    start_date: datetime
    end_date: datetime = None
    is_working: bool
    department: str = None
    position_title: str = None
    main_role: str = None

    class Config:
        from_attributes = True

class IntroductionDTO(BaseModel):
    title: str
    content: str = None

    class Config:
        from_attributes = True

class LicensesDTO(BaseModel):
    license_name: str = None
    license_agency: str = None
    license_date: datetime = None

    class Config:
        from_attributes = True
