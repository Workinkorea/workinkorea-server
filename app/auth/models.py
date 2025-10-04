# app/auth/models.py
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import List
import datetime


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    # google, github social site name table 추가예정
    social_site: Mapped[str] = mapped_column(String, index=True)
    passport_certi: Mapped[bool] = mapped_column(Boolean, index=True)
    # 추후 추가 예정

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
