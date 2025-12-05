# app/auth/models.py
import datetime
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    passport_certi: Mapped[bool] = mapped_column(Boolean, index=True, default=False)
    user_gubun: Mapped[str] = mapped_column(String, index=True, default="user", server_default="user")

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    resumes: Mapped[list["Resume"]] = relationship(
        "Resume", 
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_number: Mapped[str] = mapped_column(String, index=True, unique=True)
    company_name: Mapped[str] = mapped_column(String, index=True)

    company_users: Mapped[list["CompanyUser"]] = relationship("CompanyUser", back_populates="company")
    company_profile: Mapped["CompanyProfile"] = relationship(
        "CompanyProfile", 
        back_populates="company",
        uselist=False, 
        cascade="all, delete-orphan"
        )
    company_posts: Mapped[list["CompanyPost"]] = relationship(
        "CompanyPost",
        back_populates="company",
        cascade="all, delete-orphan"
        )


class CompanyUser(Base):
    __tablename__ = "company_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)

    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str] = mapped_column(String, index=True)

    name: Mapped[str] = mapped_column(String, index=True)
    phone: Mapped[str] = mapped_column(String, index=True)

    company: Mapped["Company"] = relationship("Company", back_populates="company_users")