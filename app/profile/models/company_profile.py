from app.database import Base
from sqlalchemy import Integer, String, ForeignKey, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.auth.models import Company
import datetime

class CompanyProfile(Base):
    __tablename__ = "company_profile"
    # company_id 를 기본키로 씀.
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id"),
        index=True,
        primary_key=True
    )
    industry_type: Mapped[str] = mapped_column(String, index=True) # 산업/업종 종류
    employee_count: Mapped[int] = mapped_column(Integer, index=True) # 직원 수
    establishment_date: Mapped[datetime.date] = mapped_column(Date, index=True) # 설립일
    company_type: Mapped[str] = mapped_column(String, index=True) # 주식회사, 유한회사 등
    insurance: Mapped[str] = mapped_column(String, index=True) # 4대 보험
    phone_number: Mapped[int] = mapped_column(BigInteger, index=True) # 대표전화번호
    address: Mapped[str] = mapped_column(String, index=True) # 주소
    website_url: Mapped[str] = mapped_column(String, index=True) # 홈페이지 주소
    email: Mapped[str] = mapped_column(String, index=True) # 대표 이메일

    company: Mapped["Company"] = relationship("Company", back_populates="company_profile")
