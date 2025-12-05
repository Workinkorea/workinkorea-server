from pydantic import BaseModel, Field, field_validator
from app.minio.minio_config import FileType


class MinioFileRequest(BaseModel):
    """통합 파일 업로드 URL 요청"""
    file_type: FileType = Field(..., description="파일 타입")
    file_name: str = Field(..., description="파일명")
    content_type: str = Field(..., description="Content-Type")
    max_size: int = Field(..., description="최대 파일 크기 (MB)")

    class Config:
        from_attributes = True


class MinioFileResponse(BaseModel):
    """파일 업로드 URL 응답"""
    url: str
    key: str
    content_type: str
    form_data: dict
    expires: str

    class Config:
        from_attributes = True

class MinioFileUrlDTO(BaseModel):
    url: str
    key: str
    content_type: str
    form_data: dict
    expires: str

    class Config:
        from_attributes = True