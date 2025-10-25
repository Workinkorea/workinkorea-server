from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.profile.models import *

# router
from app.auth.router import router as auth_router

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_router)
app.include_router(auth_router)
