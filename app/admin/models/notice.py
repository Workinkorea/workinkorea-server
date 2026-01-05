from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey

if TYPE_CHECKING:
    from app.auth.models import User

class Notice(Base):
    __tablename__ = "notices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True) # 공지 활성화/비활성화 -> 가려놓기 기능
    
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True) # 작성한 담당자
    author: Mapped["User"] = relationship("User")
