from app.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Date, Boolean

class Schools(Base):
    __tablename__ = "schools"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"), index=True)
    school_name: Mapped[str] = mapped_column(String, index=True)
    major_name: Mapped[str] = mapped_column(String, index=True)
    start_date: Mapped[datetime] = mapped_column(Date, index=True)
    end_date: Mapped[datetime] = mapped_column(Date, index=True, nullable=True)
    is_graduated: Mapped[bool] = mapped_column(Boolean, index=True)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="schools")