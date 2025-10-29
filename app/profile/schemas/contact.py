from pydantic import BaseModel
from typing import Optional


class ContactDTO(BaseModel):
    user_id: int
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateContactRequest(BaseModel):
    user_id: int
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True


class ContactResponse(BaseModel):
    user_id: int
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True