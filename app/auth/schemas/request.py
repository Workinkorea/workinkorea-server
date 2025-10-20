# app/auth/schemas.py

from pydantic import BaseModel
from datetime import date


class SignupRequest(BaseModel):
    email: str
    name: str
    birth_date: date
    country_code: str