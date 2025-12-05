from app.database import Base
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class DiagnosisAnswer(Base):
    __tablename__ = "diagnosis_answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    total_score: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    q1_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q2_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q3_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q4_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q5_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q6_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q7_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q8_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q9_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q10_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q11_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q12_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q13_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q14_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    q15_answer: Mapped[str] = mapped_column(String, index=True, nullable=True)
    