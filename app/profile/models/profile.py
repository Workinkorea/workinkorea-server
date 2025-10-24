import datetime
from typing import Optional
from app.database import Base
from app.auth.models import User
from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Profile(Base):
    __tablename__ = "profiles"
    # user_id 를 기본키로 씀.
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, primary_key=True)
    profile_image_url: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    # location 과 address 는 논의가 필요함 -> 그냥 국가코드로 퉁칠건지 아니면 디테일하게 만들건지...
    location: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    introduction: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)    
    address: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)

    # 이건 프론트에서 ENUM 확인해서 기본값 설정해야 함.
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), index=True, nullable=True)
    job_status: Mapped[str] = mapped_column(String, index=True, nullable=True) # 이것도 프론트에서 ENUM 확인.
    portfolio_url: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True) 

    birth_date: Mapped[datetime.date] = mapped_column(Date, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)

    user: Mapped["User"] = relationship("User", back_populates="profile")
    country: Mapped["Country"] = relationship("Country", back_populates="profile")
    contact: Mapped["Contact"] = relationship("Contact", back_populates="profile")
    position: Mapped["Position"] = relationship("Position", back_populates="profile")
    account_config: Mapped["AccountConfig"] = relationship("AccountConfig", back_populates="profile")


class Country(Base):
    __tablename__ = "countries"
    # user_id 를 기본키로 씀.
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("profiles.user_id", ondelete="CASCADE"),
        index=True,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String, index=True)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="country")


class Position(Base):
    __tablename__ = "positions"
    # user_id 를 기본키로 씀.
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("profiles.user_id", ondelete="CASCADE"),
        index=True,
        primary_key=True
    )
    lv1_name: Mapped[str] = mapped_column(String, index=True)
    lv2_name: Mapped[str] = mapped_column(String, index=True)
    lv3_name: Mapped[str] = mapped_column(String, index=True)
    lv4_name: Mapped[str] = mapped_column(String, index=True)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="position")
