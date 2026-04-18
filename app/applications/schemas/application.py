from pydantic import BaseModel
from datetime import datetime


class ApplicationDTO(BaseModel):
    id: int
    user_id: int
    company_post_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationRequest(BaseModel):
    company_post_id: int


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company_post_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicantUserInfo(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class ApplicantResponse(BaseModel):
    id: int
    user_id: int
    company_post_id: int
    status: str
    created_at: datetime
    user: ApplicantUserInfo

    class Config:
        from_attributes = True
