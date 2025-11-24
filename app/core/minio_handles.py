from minio import Minio
from app.core.settings import SETTINGS
from minio.datatypes import PostPolicy


import uuid
import datetime

minio_client = Minio(
    endpoint=SETTINGS.MINIO_ENDPOINT,
    access_key=SETTINGS.MINIO_ACCESS_KEY,
    secret_key=SETTINGS.MINIO_SECRET_KEY,
    secure=True
)



class MinioHandles:
    def __init__(self):
        self.minio_client = minio_client
        self.bucket_name = SETTINGS.MINIO_BUCKET_NAME

    
    def upload_resume_file(
        self,
        user_id: int,
        file_name: str,
        file_type: str,
        content_type: str,
        max_size: int = 10,
        expires_minutes: int = 5
    ) -> str:
        """
        upload resume file
        args:
            user_id: int
            file_name: str
            file_type: str
            file_size: int
        """
        try:
            file_ext = file_name.split(".")[-1]
            object_name = f"{file_type}/{user_id}/{uuid.uuid4()}.{file_ext}"

            expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)

            policy = PostPolicy(
                bucket_name=self.bucket_name,
                expiration=expires
            )

            policy.add_equals_condition("key", object_name)
        
            # Content-Type 제한
            policy.add_equals_condition("Content-Type", content_type)
            
            # 파일 크기 제한(MB)
            policy.add_content_length_range_condition(1, max_size * 1024 * 1024)

            # success_action_status 제한
            policy.add_equals_condition("success_action_status", "201")
            
            # presigned post policy 생성
            form_data = self.minio_client.presigned_post_policy(policy)

            return {
                "url": f"{SETTINGS.MINIO_ENDPOINT}/{self.bucket_name}",
                "fields": form_data,
                "object_name": object_name,
                "expires": expires.isoformat()
            }
        except Exception as e:
            raise e
