from app.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Date, Boolean, Text

class CareerHistory(Base):
    __tablename__ = "career_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"), index=True)
    company_name: Mapped[str] = mapped_column(String, index=True)
    start_date: Mapped[datetime] = mapped_column(Date, index=True)
    end_date: Mapped[datetime] = mapped_column(Date, index=True, nullable=True)
    is_working: Mapped[bool] = mapped_column(Boolean, index=True)
    department: Mapped[str] = mapped_column(String, index=True, nullable=True)
    position_title: Mapped[str] = mapped_column(String, index=True, nullable=True)
    main_role: Mapped[str] = mapped_column(Text, index=True, nullable=True)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="career_history")