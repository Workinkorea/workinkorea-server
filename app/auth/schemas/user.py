from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    email: str
    passport_certi: bool

    class Config:
        from_attributes = True