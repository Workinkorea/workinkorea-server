from fastapi import APIRouter
from app.posts.routers.company_post import router as company_post_router
from app.posts.routers.resume import router as resume_router

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

router.include_router(company_post_router)
router.include_router(resume_router)