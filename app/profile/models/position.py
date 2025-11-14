from typing import Optional
from app.database import Base
from sqlalchemy import Integer, String

from sqlalchemy.orm import Mapped, mapped_column, relationship


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    level: Mapped[int] = mapped_column(Integer, index=True)
    parent_id: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    code: Mapped[Optional[str]] = mapped_column(String, index=True)

    profiles: Mapped[list["Profile"]] = relationship("Profile", back_populates="position")
    company_posts: Mapped[list["CompanyPost"]] = relationship("CompanyPost", back_populates="position")
