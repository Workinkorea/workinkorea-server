from pydantic import BaseModel


class AccountConfigDTO(BaseModel):
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True


class UpdateAccountConfigRequest(BaseModel):
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True


class AccountConfigResponse(BaseModel):
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True