from pydantic import BaseModel


class CompanyResponse(BaseModel):
    id: int
    company_number: str
    company_name: str

    class Config:
        from_attributes = True


class UpdateCompanyRequest(BaseModel):
    company_name: str

    class Config:
        from_attributes = True
