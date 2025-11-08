from typing import Optional
from pydantic import BaseModel
import datetime

class UpdateProfileRequest(BaseModel):
    profile_image_url: Optional[str] = None
    location: str # 국가 선택하고 세부 지역(location)은 작성하는식?
    introduction: Optional[str] = None
    
    # address: Optional[str] = None # address 도 location 과 중복되는 것 같은데 프로필에 작성해야 하는지 확인 필요.
    
    position_id: int = None
    job_status: str = None
    portfolio_url: Optional[str] = None

    # 생일과 이름은 바꿀 수 없음.
    # birth_date: datetime.date
    # name: str
    country_id: int = None

    class Config:
        from_attributes = True


class UpdateContactRequest(BaseModel):
    # 이메일은 바꿀 수 없게 해야함 (아이디로 사용.)
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None


class UpdateAccountConfigRequest(BaseModel):
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True


class SelectCompanyIdRequest(BaseModel):
    company_id: int

class CompanyProfileRequest(BaseModel):
    industry_type: str
    employee_count: int
    establishment_date: datetime.date
    company_type: str
    insurance: str
    phone_number: int
    address: str
    website_url: str
    email: str

