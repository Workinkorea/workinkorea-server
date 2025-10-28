from pydantic import BaseModel
from typing import Optional


class ContactDTO(BaseModel):
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateContactRequest(BaseModel):
    # 이메일은 바꿀 수 없게 해야함 (아이디로 사용.)
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True


class ContactResponse(BaseModel):
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True