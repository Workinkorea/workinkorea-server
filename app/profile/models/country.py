from app.database import Base
from sqlalchemy import Integer, String
from app.profile.models.profile import Profile
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Country(Base):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String, index=True)

    profiles: Mapped[list["Profile"]] = relationship("Profile", back_populates="country")
