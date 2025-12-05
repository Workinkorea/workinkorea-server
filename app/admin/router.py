from fastapi import APIRouter
from app.admin.routers.user import router as user_router
from app.admin.routers.company import router as company_router
from app.admin.routers.company_post import router as company_post_router


"""
어드민 전용 기능들 라우터
"""


router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

router.include_router(user_router)
router.include_router(company_router)
router.include_router(company_post_router)
