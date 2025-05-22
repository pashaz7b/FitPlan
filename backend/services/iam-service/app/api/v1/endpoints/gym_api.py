from fastapi import Depends, HTTPException, status, APIRouter
from typing import Annotated
from loguru import logger
from starlette.status import HTTP_201_CREATED

from app.domain.schemas.gym_schema import (GymVerificationStatus,
                                           GymRegisterSchema,
                                           GymRegisterResponseSchema)

from app.domain.models.coach_model import Coach
from app.mainservices.coach_login_mainservice import get_current_coach
from app.mainservices.gym_mainservice import GymMainService

gym_router = APIRouter()


@gym_router.post("/register",
                 status_code=HTTP_201_CREATED,
                 response_model=GymRegisterResponseSchema)
async def gym_register(gym_register_schema: GymRegisterSchema,
                       gym_mainservice: Annotated[GymMainService, Depends()],
                       current_coach: Coach = Depends(get_current_coach)):
    logger.info(f"[+] Registering Gym For Coach with id {current_coach.id}")
    return await gym_mainservice.gym_register(current_coach.id, gym_register_schema)
