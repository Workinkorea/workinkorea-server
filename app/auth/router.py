# app/auth/router.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}
)

@router.post("/login")
def login():
    return {"message": "login"}

@router.post("/logout")
def logout():
    return {"message": "logout"}