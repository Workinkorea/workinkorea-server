from fastapi import FastAPI, APIRouter

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

app.include_router(app_router)
app.include_router(auth_router)
