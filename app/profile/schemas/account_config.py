from pydantic import BaseModel


class AccountConfigDTO(BaseModel):
    user_id: int
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True


class UpdateAccountConfigRequest(BaseModel):
    user_id: int
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True


class AccountConfigResponse(BaseModel):
    user_id: int
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True