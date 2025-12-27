from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CompanyPostRequest(BaseModel):
    title: str
    content: str
    work_experience: str
    position_id: int
    education: str
    language: str
    employment_type: str
    work_location: str
    working_hours: int
    salary: int
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True

class CompanyPostListRequest(BaseModel):
    skip: int
    limit: int

class ResumeRequest(BaseModel):
    title: str
    profile_url: str = None
    language_skills: Optional[list["LanguageSkillRequest"]] = None
    schools: Optional[list["SchoolRequest"]] = None
    career_history: Optional[list["CareerHistoryRequest"]] = None
    introduction: Optional[list["IntroductionRequest"]] = None
    licenses: Optional[list["LicenseRequest"]] = None

    class Config:
        from_attributes = True

class LanguageSkillRequest(BaseModel):
    language_type: Optional[str] = None
    level: Optional[str] = None

class SchoolRequest(BaseModel):
    school_name: str
    major_name: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_graduated: bool

class CareerHistoryRequest(BaseModel):
    company_name: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_working: bool
    department: Optional[str] = None
    position_title: Optional[str] = None
    main_role: Optional[str] = None

class IntroductionRequest(BaseModel):
    title: str
    content: Optional[str] = None

class LicenseRequest(BaseModel):
    license_name: Optional[str] = None
    license_agency: Optional[str] = None
    license_date: Optional[datetime] = None