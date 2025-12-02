import jwt
from app.auth.models import User
from fastapi import Depends, HTTPException, status
from app.core.settings import SETTINGS
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.repositories.auth import AuthRepository
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def get_auth_repository(
    session: AsyncSession = Depends(get_async_session)
) -> AuthRepository:
    return AuthRepository(session)



"""
어드민 전용 기능들 디펜던시
토큰으로 어드민 유저 체크
"""


async def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    auth_repository: AuthRepository = Depends(get_auth_repository)
) -> User:
    """
    현재 어드민 유저 체크 (어드민 전용 토큰 시스템)
    ADMIN JWT 토큰 검증하고 user_gubun='admin' 및 어드민 이메일 리스트 이중 체크
    args:
        credentials: HTTPAuthorizationCredentials
        auth_repository: AuthRepository
    returns:
        User
    raises:
        HTTPException
    """
    access_token = credentials.credentials
    env_admin_emails: str = SETTINGS.ADMIN_EMAILS

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # 어드민 전용 jwt secret과 알고리즘 갖고 검증함
    if not SETTINGS.ADMIN_JWT_SECRET or not SETTINGS.ADMIN_JWT_ALGORITHM:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin JWT configuration not found"
        )

    try:
        payload = jwt.decode(
            access_token,
            SETTINGS.ADMIN_JWT_SECRET,
            algorithms=[SETTINGS.ADMIN_JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # 어드민 토큰 타입 체크
        if token_type != "admin_access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin token type"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = await auth_repository.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # user_gubun이 'admin'인지 체크
    if user.user_gubun != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required - invalid user type"
        )

    # 어드민 이메일 리스트에 있는지 체크 (이중 체크)
    if not SETTINGS.ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin emails not configured"
        )

    admin_emails = [email.strip() for email in env_admin_emails.split(",")]
    if user.email not in admin_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required - email not authorized"
        )

    return user
