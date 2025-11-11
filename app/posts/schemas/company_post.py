from pydantic import BaseModel
from datetime import datetime

class CompanyPostDTO(BaseModel):
    id: int
    company_id: int
    title: str
    content: str
    work_experience: int
    position_id: int
    education: str
    language: str
    employment_type: str
    work_location: str
    working_hours: int
    salary: int
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True