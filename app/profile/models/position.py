from app.database import Base
from sqlalchemy import Integer, String
from app.profile.models.profile import Profile
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lv1_name: Mapped[str] = mapped_column(String, index=True)
    lv2_name: Mapped[str] = mapped_column(String, index=True)
    lv3_name: Mapped[str] = mapped_column(String, index=True)
    lv4_name: Mapped[str] = mapped_column(String, index=True)

    profiles: Mapped[list["Profile"]] = relationship("Profile", back_populates="position")
