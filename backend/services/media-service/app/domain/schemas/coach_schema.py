from pydantic import BaseModel


class CoachBaseSchema(BaseModel):
    email: str
