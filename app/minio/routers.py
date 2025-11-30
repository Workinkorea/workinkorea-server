from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from app.minio.schemas import MinioFileRequest, MinioFileResponse, MinioFileUrlDTO
from app.minio.minio_handles import MinioHandles
from app.minio.minio_config import FILE_TYPE_CONFIG

from app.auth.models import Company, User
from app.auth.dependencies import get_current_company_user, get_current_user


def get_minio_handles() -> MinioHandles:
    return MinioHandles()


router = APIRouter(
    prefix="/api/minio",
    tags=["minio"]
)


@router.post("/company/file")
async def upload_company_image(
    payload: MinioFileRequest,
    company: Company = Depends(get_current_company_user),
    minio_handles: MinioHandles = Depends(get_minio_handles)
) -> JSONResponse:
    """
    upload company image
    """
    try:
        config = FILE_TYPE_CONFIG.get(payload.file_type)
        file_data = payload.model_dump()

        if not config:
            return JSONResponse(content={"error": "file_type is invalid"}, status_code=400)
        if not file_data['file_name']:
            return JSONResponse(content={"error": "file_name is required"}, status_code=400)
        if not file_data['content_type']:
            return JSONResponse(content={"error": "content_type is required"}, status_code=400)
        if file_data['content_type'] not in config['allowed_content_types']:
            return JSONResponse(content={"error": "content_type is invalid"}, status_code=400)
        if file_data['max_size'] >= config['max_size_mb']:
            return JSONResponse(content={"error": "max_size is too large"}, status_code=400)
        minio_data: MinioFileUrlDTO | None = await minio_handles.upload_file_url(company.id, file_data['file_name'], config['minio_path'], file_data['content_type'], file_data['max_size'])
        if not minio_data:
            return JSONResponse(content={"error": "failed to upload file"}, status_code=400)
        return MinioFileResponse.model_validate(minio_data)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/user/file")
async def upload_user_image(
    payload: MinioFileRequest,
    user: User = Depends(get_current_user),
    minio_handles: MinioHandles = Depends(get_minio_handles)
) -> MinioFileResponse:
    """
    upload user image
    """
    try:
        config = FILE_TYPE_CONFIG.get(payload.file_type)
        file_data = payload.model_dump()
        if not config:
            return JSONResponse(content={"error": "file_type is invalid"}, status_code=400)
        if not file_data['file_name']:
            return JSONResponse(content={"error": "file_name is required"}, status_code=400)
        if not file_data['content_type']:
            return JSONResponse(content={"error": "content_type is required"}, status_code=400)
        if file_data['content_type'] not in config['allowed_content_types']:
            return JSONResponse(content={"error": "content_type is invalid"}, status_code=400)
        if file_data['max_size'] >= config['max_size_mb']:
            return JSONResponse(content={"error": "max_size is too large"}, status_code=400)
        minio_data: MinioFileUrlDTO | None = await minio_handles.upload_file_url(user.id, file_data['file_name'], config['minio_path'], file_data['content_type'], file_data['max_size'])
        if not minio_data:
            return JSONResponse(content={"error": "failed to upload file"}, status_code=400)
        return MinioFileResponse.model_validate(minio_data)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
