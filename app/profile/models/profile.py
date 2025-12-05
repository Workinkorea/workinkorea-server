import datetime
from typing import Optional, List, Dict, Any
from app.database import Base
from app.auth.models import User
from sqlalchemy import Integer, String, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CareerEnum(str, Enum):
    """경력 구분"""
    NEWCOMER = "신입"  # 신입
    YEAR_1_LESS = "1년 이하"  # 1년 이하
    YEAR_1 = "1년"  # 1년
    YEAR_2_LESS = "2년 이하"  # 2년 이하
    YEAR_2 = "2년"  # 2년
    YEAR_3_LESS = "3년 이하"  # 3년 이하
    YEAR_3 = "3년"  # 3년
    YEAR_5_LESS = "5년 이하"  # 5년 이하
    YEAR_5 = "5년"  # 5년
    YEAR_7_LESS = "7년 이하"  # 7년 이하
    YEAR_7 = "7년"  # 7년
    YEAR_10_LESS = "10년 이하"  # 10년 이하
    YEAR_10 = "10년"  # 10년
    YEAR_10_MORE = "10년 이상"  # 10년 이상


class Profile(Base):
    __tablename__ = "profiles"
    # user_id 를 기본키로 씀.
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        primary_key=True
    )
    profile_image_url: Mapped[Optional[str]] = mapped_column(
        String, index=True, nullable=True)
    # location 과 address 는 논의가 필요함 -> 그냥 국가코드로 퉁칠건지 아니면 디테일하게 만들건지...
    location: Mapped[Optional[str]] = mapped_column(
        String, index=True, nullable=True)
    introduction: Mapped[Optional[str]] = mapped_column(
        String, index=True, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(
        String, index=True, nullable=True)

    language_skills: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(
        JSONB,
        nullable=True,
        default=list
    )

    position_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("positions.id"),
        index=True,
        nullable=True
    )
    career: Mapped[Optional[str]] = mapped_column(
        SQLEnum(CareerEnum, native_enum=False, length=20),
        index=True,
        nullable=True
    )  # 경력
    job_status: Mapped[str] = mapped_column(String, index=True, nullable=True)
    portfolio_url: Mapped[Optional[str]] = mapped_column(
        String, index=True, nullable=True)

    birth_date: Mapped[datetime.date] = mapped_column(Date, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"), index=True)

    user: Mapped["User"] = relationship("User", back_populates="profile")
    country: Mapped["Country"] = relationship(
        "Country", back_populates="profiles")
    contact: Mapped["Contact"] = relationship(
        "Contact", back_populates="profile")
    position: Mapped["Position"] = relationship(
        "Position", back_populates="profiles")
    account_config: Mapped["AccountConfig"] = relationship(
        "AccountConfig", back_populates="profile")
