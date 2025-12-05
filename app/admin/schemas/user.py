from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: int
    email: str
    passport_certi: bool

    class Config:
        from_attributes = True


class UpdateUserRequest(BaseModel):
    passport_certi: Optional[bool] = None

    class Config:
        from_attributes = True
