from app.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date
from datetime import datetime

class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    profile_url: Mapped[str] = mapped_column(String, index=True, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="resumes")
    language_skills: Mapped[list["LanguageSkills"]] = relationship(
        "LanguageSkills", 
        back_populates="resume",
        cascade="all, delete-orphan"
    )
    schools: Mapped[list["Schools"]] = relationship(
        "Schools", 
        back_populates="resume",
        cascade="all, delete-orphan"
    )
    career_history: Mapped[list["CareerHistory"]] = relationship(
        "CareerHistory", 
        back_populates="resume",
        cascade="all, delete-orphan"
    )
    introduction: Mapped[list["Introduction"]] = relationship(
        "Introduction", 
        back_populates="resume",
        cascade="all, delete-orphan"
    )
    licenses: Mapped[list["Licenses"]] = relationship(
        "Licenses", 
        back_populates="resume",
        cascade="all, delete-orphan"
    )