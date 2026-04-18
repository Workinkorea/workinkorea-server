from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.auth.models import User
from app.auth.dependencies import get_current_user

from app.applications.services.application import ApplicationService
from app.applications.schemas.application import ApplicationRequest, ApplicationResponse

router = APIRouter()


def get_application_service(session: AsyncSession = Depends(get_async_session)):
    return ApplicationService(session)


@router.post("", status_code=201)
async def create_application(
    payload: ApplicationRequest,
    user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    try:
        application = await service.create_application(user.id, payload.company_post_id)
        return JSONResponse(
            content=application.model_dump(mode="json"),
            status_code=201
        )
    except ValueError as e:
        status_code = 409 if "Already applied" in str(e) else 404
        return JSONResponse(content={"error": str(e)}, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/me")
async def get_my_applications(
    user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    try:
        applications = await service.get_my_applications(user.id)
        return JSONResponse(
            content={"applications": [a.model_dump(mode="json") for a in applications]},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/{application_id}")
async def cancel_application(
    application_id: int,
    user: User = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service),
):
    try:
        await service.cancel_application(application_id, user.id)
        return JSONResponse(content={"message": "Application cancelled"}, status_code=200)
    except PermissionError as e:
        return JSONResponse(content={"error": str(e)}, status_code=403)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
