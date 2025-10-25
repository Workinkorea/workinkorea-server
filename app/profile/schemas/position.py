from typing import Optional
from pydantic import BaseModel


class PositionDTO(BaseModel):
    id: int
    lv1_name: str
    lv2_name: str
    lv3_name: Optional[str] = None
    lv4_name: Optional[str] = None

    class Config:
        from_attributes = True
