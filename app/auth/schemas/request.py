# app/auth/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional


class SignupRequest(BaseModel):
    email: str
    name: str
    birth_date: date
    country_code: str
    password: Optional[str] = None

class EmailCertifyRequest(BaseModel):
    email: str

class EmailCertifyVerifyRequest(BaseModel):
    email: str
    code: str

class CompanySignupRequest(BaseModel):
    company_number: str
    company_name: str
    email: str
    password: str
    name: str
    phone: str

class CompanyLoginRequest(BaseModel):
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str