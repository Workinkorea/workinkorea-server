import jwt
from app.auth.models import User
from app.auth.models import CompanyUser

from fastapi import Request, Depends
from fastapi import HTTPException, status
from app.core.settings import SETTINGS

from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.repositories.auth import AuthRepository
from app.auth.repositories.company import CompanyRepository


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def get_auth_repository(
    session: AsyncSession = Depends(get_async_session)
) -> AuthRepository:
    return AuthRepository(session)

def get_company_repository(
    session: AsyncSession = Depends(get_async_session)
) -> CompanyRepository:
    return CompanyRepository(session)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    auth_repository: AuthRepository = Depends(get_auth_repository)
) -> User:
    """
    get current user
    args:
        credentials: HTTPAuthorizationCredentials
    """
    access_token = None
    if credentials:
        access_token = credentials.credentials
    if not access_token:
        access_token = request.cookies.get("access_token")
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
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired"
        )
    except jwt.InvalidSignatureError: # 어드민 토큰으로 일반 유저 api 쓰려고 할 때 발생할 수도 있음
        try: # 어드민 시크릿으로 재검증
            payload = jwt.decode(
                access_token, 
                SETTINGS.ADMIN_JWT_SECRET,
                algorithms=[SETTINGS.ADMIN_JWT_ALGORITHM]
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token signature"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail=f"Invalid token: {e}" -> 프로덕션 환경에서는 예외 상세메세지를 숨기는 편이 좋음
            detail=f"Invalid token"
        )
    email: str = payload.get("sub")
    if not email:
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


async def get_current_company_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    company_repository: CompanyRepository = Depends(get_company_repository)
) -> CompanyUser:
    """
    get current company user
    args:
        credentials: HTTPAuthorizationCredentials
    """
    access_token = credentials.credentials
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

        # token 검증
        email: str = payload.get("sub")
        company_id:str = payload.get("company_id")
        if not email or not company_id:
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
    company_user = await company_repository.get_company_user_by_email(email)
    if not company_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Company user not found"
        )
    
    company = await company_repository.get_company_by_company_id(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Company not found"
        )
    return company