from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class NoticeBase(BaseModel):
    title: str
    content: str
    is_active: bool = True

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None

class NoticeResponse(NoticeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
