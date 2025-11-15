from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.posts.services.resume import ResumeService
from app.posts.schemas.request import ResumeRequest

from app.auth.models import User
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)

def get_resume_service(session: AsyncSession = Depends(get_async_session)):
    return ResumeService(session)

@router.get("/list/me")
async def get_resume_list_by_user_id(
    user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service)
):
    """
    get resume list by user id
    """
    try:
        resume_list = await resume_service.get_resume_list_by_user_id(user.id)
        return JSONResponse(content={"resume_list": resume_list}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/{resume_id}")
async def get_resume_by_user_id(
    resume_id: int,
    resume_service: ResumeService = Depends(get_resume_service)
):
    """
    get resume by user id
    """
    try:
        resume = await resume_service.get_resume_by_resume_id(resume_id)
        return JSONResponse(content={"resume": resume}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("")
async def create_resume(
    request: ResumeRequest,
    resume_service: ResumeService = Depends(get_resume_service),
    user: User = Depends(get_current_user)
):
    """
    create resume
    """
    try:
        resume_data = request.model_dump()
        resume_data["user_id"] = user.id
        resume_id = await resume_service.create_resume(resume_data)
        return JSONResponse(content={"resume_id": resume_id}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.put("/{resume_id}")
async def update_resume(
    resume_id: int,
    request: ResumeRequest,
    resume_service: ResumeService = Depends(get_resume_service),
    user: User = Depends(get_current_user)
):
    """
    update resume
    args:
        resume_id: int
        request: ResumeRequest
    """
    try:
        resume_data = request.model_dump()
        resume_data["id"] = resume_id
        resume_id = await resume_service.update_resume(resume_data)
        return JSONResponse(content={"resume_id": resume_id}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: int,
    resume_service: ResumeService = Depends(get_resume_service)
):
    """
    delete resume
    """
    try:
        resume_id = await resume_service.delete_resume(resume_id)
        return JSONResponse(content={"message": "Resume deleted successfully"}, status_code=200)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)