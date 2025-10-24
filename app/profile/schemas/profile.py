from pydantic import BaseModel
from typing import Optional
import datetime


class ProfileDTO(BaseModel):
    profile_image_url: Optional[str] = None
    location: str
    introduction: Optional[str] = None
    # address: Optional[str] = None

    position_id: int
    job_status: str
    portfolio_url: Optional[str] = None

    birth_date: datetime.date
    name: str
    country_id: int

    class Config:
        from_attributes = True
