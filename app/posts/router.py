from fastapi import APIRouter
from app.posts.routers.company_post import router as company_post_router

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)
router.include_router(company_post_router)