# app/auth/router.py
from fastapi import APIRouter
from app.profile.routers.profile import router as profile_router
from app.profile.routers.contact import router as contact_router
from app.profile.routers.account_config import router as account_config_router


router = APIRouter(
    prefix="/api/profile",
    tags=["profile"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)
router.include_router(profile_router)
router.include_router(contact_router)
router.include_router(account_config_router)
