from typing import Annotated
from fastapi import APIRouter, Depends, status
from loguru import logger

from app.domain.schemas.token_schema import TokenDataSchema
from app.mainservices.auth_service import get_current_user
from app.domain.schemas.user_schema import (GetUserInfoSchema,
                                            SetUserInfoSchema,
                                            GetUserTransactionsSchema,
                                            GetUserCoachSchema,
                                            UserRequestExerciseSchema,
                                            UserRequestExerciseResponseSchema,
                                            GetUserExerciseSchema, UserRequestMealResponseSchema, UserRequestMealSchema,
                                            GetUserMealSchema, GetUserAllCoachSchema,
                                            UserTakeWorkoutCoachResponseSchema, UserTakeWorkoutCoachSchema)

from app.mainservices.user_mainservice import UserMainService

user_core_router = APIRouter()


# @ocr_router.post(
#     "/process", response_model=OCRCreateResponse, status_code=status.HTTP_201_CREATED
# )
# async def process_image(
#     ocr_create: OCRCreateRequest,
#     current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
#     ocr_service: Annotated[OCRService, Depends()]
# ):
#     logger.info(f'Processing image {ocr_create.image_id} for user {current_user.id}')
#     return await ocr_service.process_image(ocr_create, current_user.id)
#
#
# @ocr_router.post(
#     "/get_ocr_result", response_model=OCRResponse, status_code=status.HTTP_200_OK
# )
# async def get_ocr_result(
#     ocr_request: OCRRequest,
#     current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
#     ocr_service: Annotated[OCRService, Depends()]
# ):
#     return await ocr_service.get_ocr_result(ocr_request, current_user.id)
#
#
# @ocr_router.get(
#     "/get_ocr_history", response_model=list[OCRResponse], status_code=status.HTTP_200_OK
# )
# async def get_ocr_history(
#     current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
#     ocr_service: Annotated[OCRService, Depends()]
# ):
#     return await ocr_service.get_ocr_history(current_user.id)

@user_core_router.get(
    "/get_user_info", response_model=GetUserInfoSchema, status_code=status.HTTP_200_OK
)
async def get_user_info(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting user info for user {current_user.id}')
    return await user_service.get_user_info(current_user.id)


@user_core_router.put(
    "/change_user_info",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def change_user_info(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_data: SetUserInfoSchema,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Changing user info for user {current_user.id}')
    return await user_service.change_user_info(current_user.id, user_data)


@user_core_router.get(
    "/get_user_all_coach",
    status_code=status.HTTP_200_OK,
    response_model=list[GetUserAllCoachSchema]
)
async def get_user_all_coach(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting all coach for user {current_user.id}')
    return await user_service.get_user_all_coach(current_user.id)


@user_core_router.post(
    "/set_user_workout_coach",
    status_code=status.HTTP_201_CREATED,
    response_model=UserTakeWorkoutCoachResponseSchema
)
async def set_user_workout_coach(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_schema: UserTakeWorkoutCoachSchema,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Setting workout coach for user {current_user.id}')
    return await user_service.create_user_take_workout_coach(current_user.id, user_schema)


@user_core_router.get(
    "/get_user_transactions",
    status_code=status.HTTP_200_OK,
    response_model=list[GetUserTransactionsSchema]
)
async def get_user_transactions(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting user transactions for user {current_user.id}')
    return await user_service.get_user_transaction_log(current_user.id)


@user_core_router.get(
    "/get_user_coach",
    status_code=status.HTTP_200_OK,
    response_model=GetUserCoachSchema
)
async def get_user_coach(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting user coach for user {current_user.id}')
    return await user_service.get_user_coach(current_user.id)


@user_core_router.post(
    "/request_exercise",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRequestExerciseResponseSchema
)
async def request_exercise(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_schema: UserRequestExerciseSchema,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Requesting exercise for user {current_user.id}')
    return await user_service.create_user_exercise(current_user.id, user_schema)


@user_core_router.get(
    "/user_get_exercise",
    status_code=status.HTTP_200_OK,
    response_model=list[GetUserExerciseSchema]
)
async def user_get_exercise(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting exercise for user {current_user.id}')
    return await user_service.get_user_exercise(current_user.id)


@user_core_router.post(
    "/request_meal",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRequestMealResponseSchema
)
async def request_meal(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_schema: UserRequestMealSchema,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Requesting meal for user {current_user.id}')
    return await user_service.create_user_meal(current_user.id, user_schema)


@user_core_router.get(
    "/user_get_meal",
    status_code=status.HTTP_200_OK,
    response_model=GetUserMealSchema
)
async def user_get_meal(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting meal for user {current_user.id}')
    return await user_service.get_user_meal(current_user.id)


@user_core_router.get(
    "/get_user_all_coach_free",
    status_code=status.HTTP_200_OK,
    response_model=list[GetUserAllCoachSchema]
)
async def get_user_all_coach_free(
        user_service: Annotated[UserMainService, Depends()]
):
    current_user_id = 1
    logger.info(f'[...] Getting all coach for user')
    return await user_service.get_user_all_coach(current_user_id)
