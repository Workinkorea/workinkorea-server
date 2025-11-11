from typing import Optional
from app.database import Base
from sqlalchemy import Integer, String

from sqlalchemy.orm import Mapped, mapped_column, relationship


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lv1_name: Mapped[str] = mapped_column(String, index=True)
    lv2_name: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    lv3_name: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    lv4_name: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)

    profiles: Mapped[list["Profile"]] = relationship("Profile", back_populates="position")
    company_posts: Mapped[list["CompanyPost"]] = relationship("CompanyPost", back_populates="position")
