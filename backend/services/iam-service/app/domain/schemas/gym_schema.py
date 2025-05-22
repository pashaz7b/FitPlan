from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class GymVerificationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class GymRegisterSchema(BaseModel):
    name: str
    license_number: str
    license_image: Optional[str] = None
    location: Optional[str] = None
    image: Optional[str] = None
    sport_facilities: Optional[str] = None
    welfare_facilities: Optional[str] = None


class GymRegisterResponseSchema(BaseModel):
    message: str
    verification_status: GymVerificationStatus
    created_at: datetime
    updated_at: datetime
