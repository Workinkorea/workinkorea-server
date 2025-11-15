from app.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Date

class Licenses(Base):
    __tablename__ = "licenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"), index=True)
    license_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    license_agency: Mapped[str] = mapped_column(String, index=True, nullable=True)
    license_date: Mapped[datetime] = mapped_column(Date, index=True, nullable=True)
    
    resume: Mapped["Resume"] = relationship("Resume", back_populates="licenses")