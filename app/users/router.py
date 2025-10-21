# app/auth/router.py
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import Request

from app.core.settings import SETTINGS
from urllib.parse import urlencode

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db

from app.auth.service import *
from app.auth.schemas.request import *


router = APIRouter(
    prefix="/api/users",
    tags=["auth"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)
