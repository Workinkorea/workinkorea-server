from pydantic import BaseModel


class UserEmailDTO(BaseModel):
    user_id: int
    email: str


class BulkEmailSendRequest(BaseModel):
    subject: str
    title: str
    content: str


class BulkEmailSendResponse(BaseModel):
    message: str
    sent_count: int
