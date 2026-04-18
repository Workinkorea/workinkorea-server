from fastapi import APIRouter
from app.applications.routers.application import router as application_router

router = APIRouter(prefix="/api/applications", tags=["applications"])
router.include_router(application_router)
