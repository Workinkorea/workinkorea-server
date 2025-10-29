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

class EmailCertifyVerifyRequest(BaseModel):
    email: str
    code: str

class CompanySignupRequest(BaseModel):
    company_number: int
    company_name: str
    email: str
    password: str
    name: str
    phone: int

class CompanyLoginRequest(BaseModel):
    email: str
    password: str