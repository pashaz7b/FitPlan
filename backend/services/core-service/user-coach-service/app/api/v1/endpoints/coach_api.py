from typing import Annotated
from fastapi import APIRouter, Depends, status
from loguru import logger

from app.domain.schemas.token_schema import TokenDataSchema
from app.mainservices.coach_auth_service import get_current_coach
from app.domain.schemas.coach_schema import (GetCoachUserSchema, GetCoachUserMealRequestSchema, SetCoachUserMealSchema,
                                             SetCoachUserMealResponseSchema)

from app.mainservices.coach_mainservice import CoachMainService

coach_core_router = APIRouter()


@coach_core_router.get(
    "/get_coach_user",
    response_model=list[GetCoachUserSchema],
    status_code=status.HTTP_200_OK
)
async def get_coach_user(
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        coach_service: Annotated[CoachMainService, Depends()]
):
    logger.info(f'Get all user for coach {current_coach.id}')
    return await coach_service.get_coach_user(current_coach.id)


@coach_core_router.get(
    "/get_user_meal_request",
    response_model=list[GetCoachUserMealRequestSchema],
    status_code=status.HTTP_200_OK
)
async def get_coach_user_meal_request(
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        coach_service: Annotated[CoachMainService, Depends()]
):
    logger.info(f'Get all meal request for coach {current_coach.id}')
    return await coach_service.get_coach_user_meal_request(current_coach.id)


@coach_core_router.post(
    "/accept_meal_request",
    response_model=SetCoachUserMealResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def accept_meal_request(
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        set_coach_user_meal: SetCoachUserMealSchema,
        coach_service: Annotated[CoachMainService, Depends()]
):
    logger.info(f'Accept and send meal Plan With Coach id --->{current_coach.id}')
    return await coach_service.create_coach_user_meal(current_coach.id, set_coach_user_meal)
