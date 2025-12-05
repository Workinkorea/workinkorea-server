from app.database import Base

from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AccountConfig(Base):
    __tablename__ = "account_config"
    # user_id 를 기본키로 씀.
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("profiles.user_id", ondelete="CASCADE"),
        index=True,
        primary_key=True
    )
    sns_message_notice: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    email_notice: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="account_config")