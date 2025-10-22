# app/auth/models.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Date, Boolean
from app.database import Base
import datetime

from app.auth.models import RefreshToken


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    passport_certi: Mapped[bool] = mapped_column(Boolean, index=True)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship("RefreshToken", back_populates="user")
    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")
    contacts: Mapped["Contact"] = relationship("Contact", back_populates="user")


class Country(Base):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String, index=True)

    profiles: Mapped[list["Profile"]] = relationship("Profile", back_populates="country")


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    profile_image_url: Mapped[str] = mapped_column(String, index=True, nullable=True)
    location: Mapped[str] = mapped_column(String, index=True, nullable=True)
    introduction: Mapped[str] = mapped_column(String, index=True, nullable=True)    
    address: Mapped[str] = mapped_column(String, index=True, nullable=True)

    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), index=True, nullable=True)
    job_status: Mapped[str] = mapped_column(String, index=True, nullable=True)
    portfolio_url: Mapped[str] = mapped_column(String, index=True, nullable=True)

    birth_date: Mapped[datetime.date] = mapped_column(Date, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)

    country: Mapped["Country"] = relationship("Country", back_populates="profiles")
    user: Mapped["User"] = relationship("User", back_populates="profile")
    position: Mapped["Position"] = relationship("Position", back_populates="profiles")


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    phone_number: Mapped[str] = mapped_column(String, index=True, nullable=True)
    github_url: Mapped[str] = mapped_column(String, index=True, nullable=True)
    linkedin_url: Mapped[str] = mapped_column(String, index=True, nullable=True)
    website_url: Mapped[str] = mapped_column(String, index=True, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="contacts")


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lv1_name: Mapped[str] = mapped_column(String, index=True)
    lv2_name: Mapped[str] = mapped_column(String, index=True)
    lv3_name: Mapped[str] = mapped_column(String, index=True)
    lv4_name: Mapped[str] = mapped_column(String, index=True)

    profiles: Mapped[list["Profile"]] = relationship("Profile", back_populates="position")
