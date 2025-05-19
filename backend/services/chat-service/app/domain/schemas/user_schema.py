from pydantic import BaseModel
from datetime import datetime

class UserCreateChatSchema(BaseModel):
    content: str

class UserCreateChatResponseSchema(BaseModel):
    user_id: int
    coach_id: int
    content: str
    sender_type: str  # "user"
    receiver_type: str  # "coach"
    id: int
    date: datetime
    created_at: datetime

    class Config:
        orm_mode = True
