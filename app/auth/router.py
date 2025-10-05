# app/auth/router.py
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import Request

from app.core.settings import SETTINGS
from urllib.parse import urlencode
import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db

from app.auth.service import *


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)


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
        return {"url": url}
    except Exception as e:
        return {"error": str(e)}


@router.get("/login/google/test")
async def login_google_test():
    """
    google login test
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
async def login_google_callback(code: str, db: AsyncSession = Depends(get_async_db)):
    """
    google login callback
    """
    try:
        token_data = {
            "code": code,
            "client_id": SETTINGS.GOOGLE_CLIENT_ID,
            "client_secret": SETTINGS.GOOGLE_CLIENT_SECRET,
            "redirect_uri": SETTINGS.GOOGLE_REDIRECT_URI,
            "code": code,
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
        user = await get_user_by_email(user_info_data['email'], db)
        status_massage_dict = {"status": "success"}

        if not user:
            # user 생성
            user_info_data['social_site'] = 'google'
            user = await create_user_by_social(user_info_data, db)
            status_massage_dict["status"] = "signup"
            if not user:
                status_massage = urlencode(
                    {"status": "error", "message": "Failed to create user"})
                url = f"{SETTINGS.CLIENT_URL}?{status_massage}"
                return RedirectResponse(url=url)

        # jwt token 생성
        access_token = await create_access_token(user.email)
        refresh_token = await create_refresh_token(user.email)

        # 회원가입 / 로그인 구분
        if status_massage_dict["status"] == "signup":
            status_massage_dict["name"] = user.name
        else:
            status_massage_dict["token"] = access_token

        # jwt refresh token db 저장
        refresh_token_obj = await create_refresh_token_to_db(refresh_token, user.id, db)
        if not refresh_token_obj:
            status_massage = urlencode(
                {"status": "error", "message": "Failed to create refresh token"})
            url = f"{SETTINGS.CLIENT_URL}/auth/callback?{status_massage}"
            return RedirectResponse(url=url)

        # jwt token 쿠키에 저장
        success_url = f"{SETTINGS.CLIENT_URL}?{urlencode(status_massage_dict)}"
        response = RedirectResponse(url=success_url)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # 개발 환경에서는 secure=False
            max_age=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES,
            samesite="none",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,  # 개발 환경에서는 secure=False
            max_age=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES,
            samesite="none",
        )
        return response
    except Exception as e:
        status_massage = urlencode({"status": "error", "message": str(e)})
        url = f"{SETTINGS.CLIENT_URL}/auth/callback?{status_massage}"
        return RedirectResponse(url=url)


@router.delete("/logout")
async def logout(request: Request, db: AsyncSession = Depends(get_async_db)):
    """
    logout delete refresh token from db and delete cookies
    """
    try:
        result = await delete_refresh_token_from_db(request.cookies.get("refresh_token"), db)
        if not result:
            return JSONResponse(content={"message": "Refresh token not found"}, status_code=401)

        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except Exception as e:
        return {"error": str(e)}


@router.post("/refresh")
async def refresh(request: Request):
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
        access_token = await create_access_token(user_email)
        if not access_token:
            return JSONResponse(content={"message": "Failed to create access token"}, status_code=500)

        response = JSONResponse(content={"message": "Access token refreshed"})

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            max_age=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES,
            samesite="none"
        )
        return response
    except Exception as e:
        return {"error": str(e)}
