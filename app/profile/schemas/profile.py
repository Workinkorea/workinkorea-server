from pydantic import BaseModel
from typing import Optional
import datetime


class ProfileDTO(BaseModel):
    user_id: int
    profile_image_url: Optional[str] = None
    location: Optional[str] = None
    introduction: Optional[str] = None

    address: Optional[str] = None # 상세 주소

    position_id: Optional[int] = None
    job_status: Optional[str] = None
    portfolio_url: Optional[str] = None

    birth_date: datetime.date
    name: str
    country_id: int

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    user_id: int
    profile_image_url: Optional[str] = None
    location: Optional[str] = None # 현재 거주중인 도시/위치 등
    introduction: Optional[str] = None
    address: Optional[str] = None # 상세 주소
    
    position_id: Optional[int] = None
    job_status: Optional[str] = None
    portfolio_url: Optional[str] = None

    # 생일과 이름은 바꿀 수 없음.
    # birth_date: datetime.date
    # name: str
    country_id: int = None # 현재 거주중인 국가

    class Config:
        from_attributes = True


class ProfileResponse(BaseModel):
    user_id: int
    profile_image_url: Optional[str] = None
    location: Optional[str] = None
    introduction: Optional[str] = None
    address: Optional[str] = None

    position_id: Optional[int] = None
    job_status: Optional[str] = None
    portfolio_url: Optional[str] = None

    birth_date: datetime.date
    name: str
    country_id: int

    class Config:
        from_attributes = True


class UserImageRequest(BaseModel):
    file_name: str
    content_type: str
    max_size: int

    class Config:
        from_attributes = True