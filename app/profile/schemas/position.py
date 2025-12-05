from typing import Optional
from pydantic import BaseModel


class PositionDTO(BaseModel):
    id: int
    name: str
    level: int
    parent_id: Optional[int] = None
    code: Optional[str] = None

    class Config:
        from_attributes = True


class UpdatePositionRequest(BaseModel):
    id: int
    name: str
    level: int
    parent_id: Optional[int] = None
    code: Optional[str] = None

    class Config:
        from_attributes = True