from typing import Optional
from pydantic import BaseModel
import datetime


class ProfileResponse(BaseModel):
    profile_image_url: Optional[str] = None
    location: str # 국가 선택하고 세부 지역(location)은 작성하는식?
    introduction: Optional[str] = None
    # address: Optional[str] = None # address 도 location 과 중복되는 것 같은데 프로필에 작성해야 하는지 확인 필요.

    position_id: int
    job_status: str
    portfolio_url: Optional[str] = None

    birth_date: datetime.date
    name: str
    country_id: int

    class Config:
        from_attributes = True


class ContactResponse(BaseModel):
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True


class AccountConfigResponse(BaseModel):
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True

class CompanyProfileResponse(BaseModel):
    company_id: int
    industry_type: str
    employee_count: int
    establishment_date: datetime.date
    company_type: str
    insurance: str
    phone_number: int
    address: str
    website_url: str
    email: str

    class Config:
        from_attributes = True