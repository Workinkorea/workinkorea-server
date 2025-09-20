# app/auth/models.py
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any

class EmailSchema(BaseModel):
    email: List[EmailStr]