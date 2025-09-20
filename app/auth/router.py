# app/auth/router.py
from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.auth.models import EmailSchema
from app.auth.service import send_email_verifi_code

router = APIRouter(
    prefix="/api/auth",
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


@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    """
    email verification code send
    args:
        email: EmailSchema
    """
    try:
        await send_email_verifi_code(email)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     