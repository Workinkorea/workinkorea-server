from pydantic import BaseModel
from typing import Optional


class ContactDTO(BaseModel):
    user_id: int
    phone_number: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateContactRequest(BaseModel):
    """
    PATCH 요청용 스키마 - 모든 필드는 Optional이며,
    보내지 않은 필드는 업데이트되지 않습니다.
    user_id는 body에서 받지 않고, 인증된 사용자의 ID를 사용합니다.
    """
    phone_number: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True


class ContactResponse(BaseModel):
    user_id: int
    phone_number: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None

    class Config:
        from_attributes = True