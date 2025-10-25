from typing import Optional
from app.database import Base
from app.profile.models.profile import Profile
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Contact(Base):
    __tablename__ = "contacts"
    # user_id 를 기본키로 씀.
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("profiles.user_id", ondelete="CASCADE"),
        index=True,
        primary_key=True
    )
    phone_number: Mapped[Optional[str]] = mapped_column(String, default=None, index=True, nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String, default=None, index=True, nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String, default=None, index=True, nullable=True)
    website_url: Mapped[Optional[str]] = mapped_column(String, default=None, index=True, nullable=True)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="contact")
