from app.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class LanguageSkills(Base):
    __tablename__ = "language_skills"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(Integer, ForeignKey("resumes.id"), index=True)
    language_type: Mapped[str] = mapped_column(String, index=True, nullable=True)
    level: Mapped[str] = mapped_column(String, index=True, nullable=True)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="language_skills")