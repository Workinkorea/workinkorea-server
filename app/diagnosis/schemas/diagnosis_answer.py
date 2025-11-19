from pydantic import BaseModel
from typing import Optional

class DiagnosisAnswerDTO(BaseModel):
    total_score: int
    q1_answer: Optional[str] = None
    q2_answer: Optional[str] = None
    q3_answer: Optional[str] = None
    q4_answer: Optional[str] = None
    q5_answer: Optional[str] = None     
    q6_answer: Optional[str] = None
    q7_answer: Optional[str] = None
    q8_answer: Optional[str] = None
    q9_answer: Optional[str] = None
    q10_answer: Optional[str] = None
    q11_answer: Optional[str] = None
    q12_answer: Optional[str] = None
    q13_answer: Optional[str] = None
    q14_answer: Optional[str] = None
    q15_answer: Optional[str] = None

    class Config:
        from_attributes = True

class DiagnosisAnswerResponse(BaseModel):
    id: int
    total_score: int
    q1_answer: Optional[str] = None
    q2_answer: Optional[str] = None
    q3_answer: Optional[str] = None
    q4_answer: Optional[str] = None
    q5_answer: Optional[str] = None
    q6_answer: Optional[str] = None
    q7_answer: Optional[str] = None
    q8_answer: Optional[str] = None
    q9_answer: Optional[str] = None
    q10_answer: Optional[str] = None
    q11_answer: Optional[str] = None
    q12_answer: Optional[str] = None
    q13_answer: Optional[str] = None
    q14_answer: Optional[str] = None
    q15_answer: Optional[str] = None

    class Config:
        from_attributes = True