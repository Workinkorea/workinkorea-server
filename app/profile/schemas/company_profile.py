from pydantic import BaseModel
from typing import Optional
import datetime


class CompanyProfileDTO(BaseModel):
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


class SelectCompanyIdRequest(BaseModel):
    company_id: int