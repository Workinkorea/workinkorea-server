from fastapi import APIRouter
from app.applications.routers.application import router as application_router

router = APIRouter()
router.include_router(application_router, prefix="/api/applications", tags=["applications"])
