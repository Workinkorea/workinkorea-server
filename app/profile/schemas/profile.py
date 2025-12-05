from pydantic import BaseModel
from typing import Optional
import datetime

from app.posts.schemas.resume import LanguageSkillsDTO


class ProfileDTO(BaseModel):
    user_id: int
    profile_image_url: Optional[str] = None
    location: Optional[str] = None
    introduction: Optional[str] = None

    address: Optional[str] = None  # 상세 주소

    position_id: Optional[int] = None
    career: Optional[str] = None
    job_status: Optional[str] = None
    portfolio_url: Optional[str] = None
    language_skills: Optional[list[LanguageSkillsDTO]] = None

    birth_date: datetime.date
    name: str
    country_id: int

    created_at: datetime.datetime  # 가입일

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    profile_image_url: Optional[str] = None
    location: Optional[str] = None  # 현재 거주중인 도시/위치 등
    introduction: Optional[str] = None
    address: Optional[str] = None  # 상세 주소

    position_id: Optional[int] = None
    career: Optional[str] = None  # 경력
    job_status: Optional[str] = None
    portfolio_url: Optional[str] = None
    language_skills: Optional[list[LanguageSkillsDTO]] = None
    
    # 생일과 이름은 바꿀 수 없음.
    # birth_date: datetime.date
    name: Optional[str] = None
    country_id: Optional[int] = None  # 현재 거주중인 국가

    class Config:
        from_attributes = True


class ProfileResponse(BaseModel):
    profile_image_url: Optional[str] = None
    location: Optional[str] = None
    introduction: Optional[str] = None
    address: Optional[str] = None

    position_id: Optional[int] = None
    career: Optional[str] = None  # 경력
    job_status: Optional[str] = None
    portfolio_url: Optional[str] = None
    language_skills: Optional[list[LanguageSkillsDTO]] = None
    
    birth_date: datetime.date
    name: str
    country_id: int

    created_at: datetime.datetime  # 가입일

    class Config:
        from_attributes = True
