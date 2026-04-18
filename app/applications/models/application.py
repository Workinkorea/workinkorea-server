from app.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    company_post_id: Mapped[int] = mapped_column(ForeignKey("company_posts.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String, index=True, default="pending")

    user: Mapped["User"] = relationship("User", lazy="joined")
    company_post: Mapped["CompanyPost"] = relationship("CompanyPost", lazy="joined")
