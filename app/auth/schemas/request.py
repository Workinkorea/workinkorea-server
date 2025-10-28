# app/auth/schemas.py

from pydantic import BaseModel
from datetime import date


class SignupRequest(BaseModel):
    email: str
    name: str
    birth_date: date
    country_code: str

class EmailCertifyRequest(BaseModel):
    email: str

class CompanySignupRequest(BaseModel):
    company_name: str
    company_number: int
    email: str
    name: str
    phone: str
    position:str