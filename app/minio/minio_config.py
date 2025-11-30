from enum import Enum
from typing import Dict

class FileType(str, Enum):
    """업로드 가능한 파일 타입"""
    PROFILE_IMAGE = "profile_image"  # 사용자 프로필 이미지
    COMPANY_IMAGE = "company_image"  # 회사 프로필 이미지
    COMPANY_POST = "company_post"  # 채용 공고 
    RESUME_PDF = "resume_pdf"  # 이력서 PDF


class OwnerType(str, Enum):
    """파일 소유자 타입"""
    USER = "user"
    COMPANY = "company"

# 파일 타입별 설정
FILE_TYPE_CONFIG: Dict[FileType, Dict] = {
    FileType.PROFILE_IMAGE: {
        "owner_type": OwnerType.USER,
        "max_size_mb": 5 * 1024 * 1024,
        "allowed_content_types": ["image/jpeg", "image/png", "image/jpg"],
        "minio_path": "profile_image",
    },
    FileType.COMPANY_IMAGE: {
        "owner_type": OwnerType.COMPANY,
        "max_size_mb": 5 * 1024 * 1024,
        "allowed_content_types": ["image/jpeg", "image/png", "image/jpg"],
        "minio_path": "company_image",
    },
    FileType.COMPANY_POST: {
        "owner_type": OwnerType.COMPANY,
        "max_size_mb": 5 * 1024 * 1024,
        "allowed_content_types": ["image/jpeg", "image/png", "image/jpg"],
        "minio_path": "company_post",
    },
    FileType.RESUME_PDF: {
        "owner_type": OwnerType.USER,
        "max_size_mb": 10 * 1024 * 1024,
        "allowed_content_types": ["application/pdf"],
        "minio_path": "resume_pdf",
    },
}