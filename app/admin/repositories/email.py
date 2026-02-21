from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas.email import UserEmailDTO
from app.auth.models import User
from app.profile.models.account_config import AccountConfig


class EmailRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_notice_opt_in_emails(self) -> list[UserEmailDTO]:
        # -> 굳이 유저dto 반환하는 이유는 추적하기 쉽게 하기 위함
        """
        이메일 공지 수신 동의(email_notice=True) 유저 이메일 목록 조회
        """
        stmt = (
            select(User.id, User.email)
            .distinct()
            .join(AccountConfig, AccountConfig.user_id == User.id)
            .where(AccountConfig.email_notice.is_(True))
        )
        result = await self.session.execute(stmt)

        # email 빈 값 제거하고 DTO 변환
        users = result.all()
        return [
            UserEmailDTO(user_id=user_id, email=email)
            for user_id, email in users
            if email
        ]
