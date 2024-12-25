from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TokenDataSchema(BaseModel):
    id: int
    email: str
    is_verified: bool
    # first_name: str
    # last_name: str
    # mobile_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
