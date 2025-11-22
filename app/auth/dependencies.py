import jwt
from app.auth.models import User
from fastapi import Request, Depends
from app.core.settings import SETTINGS
from fastapi import HTTPException, status
from app.database import get_async_session
from app.auth.repository import AuthRepository
from sqlalchemy.ext.asyncio import AsyncSession


def get_auth_repository(
    session: AsyncSession = Depends(get_async_session)
) -> AuthRepository:
    return AuthRepository(session)


async def get_current_user(
    request: Request,
    auth_repository: AuthRepository = Depends(get_auth_repository)
) -> User:
    """
    get current user
    args:
        request: Request
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    access_token = auth_header.split(" ")[1]

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        payload = jwt.decode(
            access_token, 
            SETTINGS.JWT_SECRET,
            algorithms=[SETTINGS.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
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
    
    return user
