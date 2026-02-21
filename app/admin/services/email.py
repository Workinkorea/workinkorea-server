from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.repositories.email import EmailRepository
from app.core.settings import SETTINGS


class EmailService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.email_repository = EmailRepository(session)

    def _get_mail_config(self) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=SETTINGS.MAIL_USERNAME,
            MAIL_PASSWORD=SETTINGS.MAIL_PASSWORD,
            MAIL_FROM_NAME=SETTINGS.MAIL_FROM_NAME,
            MAIL_FROM=SETTINGS.MAIL_FROM,
            MAIL_PORT=SETTINGS.MAIL_PORT,
            MAIL_SERVER=SETTINGS.MAIL_SERVER,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=(Path(__file__).resolve().parents[1] / "templates"),
        )

    async def send_bulk_email_to_opted_users(self, subject: str, title: str, content: str) -> int:
        """
        이메일 수신 동의 유저에게 단체 메일 발송
        args:
            subject: 메일 제목
            title: 템플릿 내부 제목
            content: 템플릿 본문
        returns:
            실제 발송 대상 수
        """

        # 이메일 수신 동의 유저들 가져오기
        recipient_users = await self.email_repository.get_notice_opt_in_emails()
        if not recipient_users:
            # 수신할 유저가 없으므로 바로 종료
            return 0

        # 보낼 이메일 목적지 리스트
        recipients = [recipient.email for recipient in recipient_users]

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            template_body={"title": title, "content": content},
            subtype=MessageType.html,
        )

        fm = FastMail(self._get_mail_config())
        await fm.send_message(message, template_name="notice_email_temp.html")
        return len(recipient_users)

    async def send_notice_email_to_opted_users(self, title: str, content: str) -> int:
        """
        공지 제목/내용을 수신 동의 유저에게 단체 발송
        returns:
            실제 발송 대상 수
        """
        return await self.send_bulk_email_to_opted_users(
            subject=f"[Work In Korea] {title}",
            title=title,
            content=content,
        )
