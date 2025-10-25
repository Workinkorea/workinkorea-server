from pydantic import BaseModel
from typing import Optional


class ContactDTO(BaseModel):
    phone_number: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True
