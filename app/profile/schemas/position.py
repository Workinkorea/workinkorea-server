from typing import Optional
from pydantic import BaseModel


class PositionDTO(BaseModel):
    id: int
    lv1_name: str
    lv2_name: Optional[str] = None
    lv3_name: Optional[str] = None
    lv4_name: Optional[str] = None

    class Config:
        from_attributes = True


class UpdatePositionRequest(BaseModel):
    id: int
    lv1_name: str # 대분류
    lv2_name: Optional[str] = None # 중분류
    lv3_name: Optional[str] = None # 소분류
    lv4_name: Optional[str] = None # 세분류

    class Config:
        from_attributes = True