# app/auth/router.py
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import Request

from app.core.settings import SETTINGS
from urllib.parse import urlencode
import httpx
import re

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.database import get_redis_client
import redis.asyncio as redis

from app.auth.service import AuthRedisService
from app.auth.service import AuthService
from app.auth.schemas.request import *
from app.profile.services.profile import ProfileService
from app.auth.models import User
import jwt

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


def get_profile_service(session: AsyncSession = Depends(get_async_session)):
    return ProfileService(session)


def get_auth_service(session: AsyncSession = Depends(get_async_session)):
    return AuthService(session)

def get_auth_redis_service(redis_client: redis.Redis = Depends(get_redis_client)):
    return AuthRedisService(redis_client)

@router.get("/login/google")
async def login_google():
    """
    google login
    """
    try:
        params = {
            "client_id": SETTINGS.GOOGLE_CLIENT_ID,
            "redirect_uri": SETTINGS.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "email profile",
            "access_type": "offline",
            "prompt": "consent",
        }
        url = f"{SETTINGS.GOOGLE_AUTHORIZATION_URL}?{urlencode(params)}"
        return RedirectResponse(url)
    except Exception as e:
        return {"error": str(e)}


@router.get("/login/google/callback")
async def login_google_callback(
    code: str,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    google login callback
    """
    try:
        token_data = {
            "code": code,
            "client_id": SETTINGS.GOOGLE_CLIENT_ID,
            "client_secret": SETTINGS.GOOGLE_CLIENT_SECRET,
            "redirect_uri": SETTINGS.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        # google token 조회
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                SETTINGS.GOOGLE_TOKEN_URL,
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            token_data = token_response.json()

        # google user profile 조회
        async with httpx.AsyncClient() as client:
            user_info_response = await client.get(
                SETTINGS.GOOGLE_USER_INFO_URL,
                headers={
                    "Authorization": f"Bearer {token_data['access_token']}"}
            )
            user_info_data = user_info_response.json()

        # user 조회
        user: User | None = await auth_service.get_user_by_email(user_info_data['email'])
        if not user:
            # user 조회 실패
            status_massage = urlencode({
                "user_email": user_info_data['email']
            })
            url = f"{SETTINGS.CLIENT_URL}/signup?{status_massage}"
            return RedirectResponse(url=url)

        status_massage_dict = {"status": "success", "user_email": user.email}

        # jwt token 생성
        access_token = await auth_service.create_access_token(user.email)
        refresh_token = await auth_service.create_refresh_token(user.email)

        # 파라미터 user name, access token 저장
        status_massage_dict["user_id"] = user.id
        status_massage_dict["name"] = user.profile.name
        status_massage_dict["token"] = access_token

        # jwt refresh token db 저장 / 추후 redis 저장 예정
        refresh_token_obj = await auth_service.create_refresh_token_to_db(refresh_token, user.id)
        if not refresh_token_obj:
            status_massage = urlencode(
                {"status": "error", "message": "Failed to create refresh token"})
            url = f"{SETTINGS.CLIENT_URL}/auth/callback?{status_massage}"
            return RedirectResponse(url=url)

        # jwt token 쿠키에 저장
        success_url = f"{SETTINGS.CLIENT_URL}/auth/callback?{urlencode(status_massage_dict)}"
        response = RedirectResponse(url=success_url)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # 개발 환경에서는 secure=False
            max_age=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES,
            samesite="lax",
            domain=SETTINGS.COOKIE_DOMAIN
        )
        return response
    except Exception as e:
        status_massage = urlencode({"status": "error", "message": str(e)})
        url = f"{SETTINGS.CLIENT_URL}/auth/callback?{status_massage}"
        return RedirectResponse(url=url)


@router.post("/signup")
async def signup(
    request: SignupRequest,
    profile_service: ProfileService = Depends(get_profile_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    signup up
    """
    try:
        user_info_data = request.model_dump()

        # 유효성 검사
        if not user_info_data['email']:
            return JSONResponse(content={"error": "email is required"}, status_code=400)
        if not "@" in user_info_data['email']:
            return JSONResponse(content={"error": "email is invalid"}, status_code=400)
        

        if not user_info_data['name']:
            return JSONResponse(content={"error": "name is required"}, status_code=400)
        if not bool(re.match(r'^[a-zA-Z\s]+$', user_info_data['name'])):
            return JSONResponse(content={"error": "name is invalid"}, status_code=400)
        
        if not user_info_data['birth_date']:
            return JSONResponse(content={"error": "birth_date is required"}, status_code=400)
        if not user_info_data['country_code']:
            return JSONResponse(content={"error": "country_code is required"}, status_code=400)

        # user 조회
        user = await auth_service.get_user_by_email(user_info_data['email'])
        if user:
            # user 이미 존재하는 경우
            return JSONResponse(content={"error": "user already exists"}, status_code=400)
        
        # country 조회
        country = await profile_service.get_country_code(user_info_data['country_code'])
        if not country:
            # country 조회 실패
            return JSONResponse(content={"error": "country not found"}, status_code=400)

        user_info_data['country_id'] = country.id
        user, profile = await auth_service.create_user_by_social(user_info_data)
        if not user or not profile:
            # user 생성 실패
            return JSONResponse(content={"error": "failed to create user"}, status_code=500)
    
        return JSONResponse(content={"url": f"{SETTINGS.CLIENT_URL}/login"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/logout")
async def logout(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    """
    logout delete refresh token from db and delete cookies
    """
    try:
        result = await auth_service.delete_refresh_token_from_db(request.cookies.get("refresh_token"))
        if not result:
            return JSONResponse(content={"message": "Refresh token not found"}, status_code=401)

        response = JSONResponse(content={"message": "Logged out"})

        response.delete_cookie(
            key="refresh_token",
            domain=SETTINGS.COOKIE_DOMAIN
        )
        return response
    except Exception as e:
        return {"error": str(e)}


@router.post("/refresh")
async def refresh(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    """
    get new access token by refresh token
    """
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return JSONResponse(content={"message": "Refresh token not found"}, status_code=401)

    try:
        # refresh token 검증
        payload = jwt.decode(refresh_token, SETTINGS.JWT_SECRET, algorithms=[
                             SETTINGS.JWT_ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            return JSONResponse(content={"message": "Invalid refresh token"}, status_code=401)

        # jwt token 생성
        access_token = await auth_service.create_access_token(user_email)
        if not access_token:
            return JSONResponse(content={"message": "Failed to create access token"}, status_code=500)
        
        return JSONResponse(content={"access_token": access_token})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/email/certify")
async def email_certification(request: EmailCertifyRequest,
    auth_redis_service: AuthRedisService = Depends(get_auth_redis_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    email certification
    """
    try:
        email = request.model_dump().get("email")
        if not email:
            return JSONResponse(content={"message": "Email is required"}, status_code=400)

        # 이메일 전송
        code = await auth_service.send_email_verify_code(email)
        if not code:
            return JSONResponse(content={"message": "Failed to send email certification code"}, status_code=500)

        # 이메일 코드 저장
        set_redis = await auth_redis_service.set_email_certify_code(email, code)
        if not set_redis:
            return JSONResponse(content={"message": "Failed to set email certification code"}, status_code=500)

        return JSONResponse(content={"message": "Send email certification code"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/email/certify/verify")
async def email_certify_verify(request: EmailCertifyRequest, auth_redis_service: AuthRedisService = Depends(get_auth_redis_service)):
    """
    email certification verify
    """
    try:
        request = request.model_dump()
        if not request['email']:
            return JSONResponse(content={"message": "Email is required"}, status_code=400)

        get_redis_code = await auth_redis_service.get_email_certify_code(request['email'], request['code'])
        if not get_redis_code:
            return JSONResponse(content={"message": "Email certification code is incorrect"}, status_code=400)
        
        return JSONResponse(content={"message": "Email certification code verified"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)