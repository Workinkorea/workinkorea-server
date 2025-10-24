from pydantic import BaseModel


class AccountConfigDTO(BaseModel):
    sns_message_notice: bool
    email_notice: bool

    class Config:
        from_attributes = True