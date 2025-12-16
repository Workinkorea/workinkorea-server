from pydantic import BaseModel
from typing import Optional


class AccountConfigDTO(BaseModel):
    user_id: int
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True


class UpdateAccountConfigRequest(BaseModel):
    """
    PATCH 요청용 스키마 - 모든 필드는 Optional이며, 
    보내지 않은 필드는 업데이트되지 않습니다.
    """
    sns_message_notice: Optional[bool] = None
    email_notice: Optional[bool] = None

    class Config:
        from_attributes = True


class AccountConfigResponse(BaseModel):
    user_id: int
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True