from pydantic import BaseModel


class CountryDTO(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True


class UpdateCountryRequest(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True
