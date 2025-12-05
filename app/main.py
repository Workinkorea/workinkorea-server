from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.profile.models import *

# router
from app.auth.router import router as auth_router
from app.profile.router import router as profile_router
from app.posts.router import router as posts_router
from app.diagnosis.router import router as diagnosis_router
from app.admin.router import router as admin_router
from app.minio.routers import router as minio_router

from app.core.settings import SETTINGS

# app
app = FastAPI(
    title="WorkinKorea Server",
    description="Work in Korea Server",
    version="0.1.0",
    contact={
        "name": "WorkinKorea",
        "url": "https://workinkorea.net",
    }
)
app_router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[SETTINGS.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(posts_router)
app.include_router(diagnosis_router)
app.include_router(admin_router)
app.include_router(minio_router)
