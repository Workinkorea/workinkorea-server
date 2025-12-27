from minio import Minio
from app.core.settings import SETTINGS
from minio.datatypes import PostPolicy
from app.minio.schemas import MinioFileUrlDTO
from app.minio.minio_config import FileType

import asyncio
import uuid
import datetime

minio_client = Minio(
    endpoint=SETTINGS.MINIO_ENDPOINT,
    access_key=SETTINGS.MINIO_ACCESS_KEY,
    secret_key=SETTINGS.MINIO_SECRET_KEY,
    secure=True,
    # region="us-east-1"
)


class MinioHandles:
    def __init__(self):
        self.minio_client = minio_client
        self.bucket_name = SETTINGS.MINIO_BUCKET_NAME

    async def upload_file_url(
        self,
        user_id: int,
        file_name: str,
        minio_path: str,
        content_type: str,
        max_size: int = 10,
        expires_minutes: int = 5
    ) -> dict:
        """
        upload resume file
        args:
            user_id: int
            file_name: str
            file_type: str
            content_type: str
            max_size: int (in MB)
            expires_minutes: int
        returns:
            dict with url, key, content_type, form_data, expires
        raises:
            ValueError: for validation errors
            Exception: for MinIO/S3 errors
        """
        try:
            # Validate inputs
            if not file_name:
                raise ValueError("file_name is required")
            if not content_type:
                raise ValueError("content_type is required")
            if not SETTINGS.MINIO_ENDPOINT:
                raise ValueError("MINIO_ENDPOINT is not configured")
            if not self.bucket_name:
                raise ValueError("MINIO_BUCKET_NAME is not configured")

            file_ext = file_name.split(".")[-1] if "." in file_name else ""
            if minio_path == FileType.PROFILE_IMAGE.value or minio_path == FileType.COMPANY_IMAGE.value:
                object_name = f"{minio_path}/{user_id}"
            else:
                object_name = f"{minio_path}/{user_id}/{uuid.uuid4()}.{file_ext}"

            expires = datetime.datetime.now(
                datetime.timezone.utc) + datetime.timedelta(minutes=expires_minutes)

            policy = PostPolicy(
                bucket_name=self.bucket_name,
                expiration=expires
            )

            policy.add_equals_condition("key", object_name)

            # Content-Type 제한
            policy.add_equals_condition("Content-Type", content_type)

            # 파일 크기 제한(MB를 bytes로 변환)
            max_size_bytes = max_size * 1024 * 1024
            policy.add_content_length_range_condition(1, max_size_bytes)

            # success_action_status 제한
            policy.add_equals_condition("success_action_status", "201")

            # presigned post policy 생성
            form_data = await asyncio.wait_for(
                asyncio.to_thread(
                    self.minio_client.presigned_post_policy,
                    policy
                ),
                timeout=10.0  # 10초 타임아웃
            )

            return MinioFileUrlDTO(
                url=f"https://{SETTINGS.MINIO_ENDPOINT}/{self.bucket_name}",
                key=object_name,
                content_type=content_type,
                form_data=form_data,
                expires=expires.isoformat()
            )
        except asyncio.TimeoutError:
            raise Exception("MinIO request timed out after 10 seconds")
        except ValueError as e:
            raise e
        except Exception as e:
            raise e
