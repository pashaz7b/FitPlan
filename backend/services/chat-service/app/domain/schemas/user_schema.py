from pydantic import BaseModel
from datetime import datetime


class UserCreateChatSchema(BaseModel):
    content: str


class UserCreateChatResponseSchema(BaseModel):
    id: int
    user_id: int
    coach_id: int
    content: str
    sender_type: str
    receiver_type: str
    date: str
    created_at: datetime

    # class Config:
    #     orm_mode = True

    model_config = {
        "from_attributes": True
    }
