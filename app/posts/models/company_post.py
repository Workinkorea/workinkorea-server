from app.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime

class CompanyPost(Base):
    __tablename__ = "company_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(String, index=True)
    content_url: Mapped[str] = mapped_column(String, index=True, nullable=True) # 공고를 이미지로 사용하는 경우
    work_experience: Mapped[str] = mapped_column(String, index=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), index=True)
    education: Mapped[str] = mapped_column(String, index=True)
    language: Mapped[str] = mapped_column(String, index=True)
    employment_type: Mapped[str] = mapped_column(String, index=True)
    work_location: Mapped[str] = mapped_column(String, index=True)
    working_hours: Mapped[int] = mapped_column(Integer, index=True)
    salary: Mapped[int] = mapped_column(Integer, index=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=True)

    company: Mapped["Company"] = relationship("Company", back_populates="company_posts")
    position: Mapped["Position"] = relationship("Position", back_populates="company_posts")