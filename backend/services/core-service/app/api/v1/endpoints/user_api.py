# from select import select
from typing import Annotated
from fastapi import APIRouter, Depends, status, Request
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
                                            UserTakeWorkoutCoachResponseSchema, UserTakeWorkoutCoachSchema,
                                            GroupedExerciseSchema, ChangeUserCoach, ChangeUserCoachResponse)

from app.domain.schemas.user_schema import (UserGetAllVerifiedGymSchema,
                                            UserGetVerifiedGymDetailSchema,
                                            UserGetVerifiedGymCoachesSchema,
                                            UserGetVerifiedGymPlanPriceSchema,
                                            UserGetVerifiedGymCommentsSchema,
                                            CreateUserGymRegistrationResponseSchema,
                                            CreateUserGymRegistrationSchema,
                                            UserGetGymRegistrationsSchema,
                                            CreateUserGymCommentSchema,
                                            CreateUserGymCommentResponseSchema,
                                            UserGetVerifiedCoachCommentsSchema, UserGetCoachPlanPriceSchema,
                                            CreateUserCoachCommentSchema, CreateUserCoachCommentResponseSchema)

from app.mainservices.user_mainservice import UserMainService

user_core_router = APIRouter()


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
    response_model=list[GroupedExerciseSchema]
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
    response_model=list[GetUserMealSchema]
)
async def user_get_meal(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting meal for user {current_user.id}')
    return await user_service.get_user_meal(current_user.id)


@user_core_router.put(
    "/change_user_coach",
    status_code=status.HTTP_201_CREATED,
    response_model=ChangeUserCoachResponse
)
async def change_user_coach(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        new_workout_coach: ChangeUserCoach,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f"[+] Updating Coach For User With ID {current_user.id}")
    return await user_service.update_user_coach(current_user.id,
                                                {"workout_plan_id": new_workout_coach.new_workout_plan_id})


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


# ********************************************************************************


@user_core_router.get(
    "/get_all_verified_gyms",
    status_code=status.HTTP_200_OK,
    response_model=list[UserGetAllVerifiedGymSchema]
)
async def user_get_all_verified_gyms(
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Getting All Verified Gyms For User')
    return await user_service.user_get_all_verified_gyms()


@user_core_router.get(
    "/get_verified_gym_detail",
    status_code=status.HTTP_200_OK,
    response_model=UserGetVerifiedGymDetailSchema
)
async def user_get_verified_gym_detail(
        request: Request,
        user_service: Annotated[UserMainService, Depends()],
        gym_id: int
):
    user_ip = request.client.host
    logger.info(f'[...] Getting Verified Gym Detail For User {user_ip}')
    return await user_service.user_get_verified_gym_detail(gym_id)


@user_core_router.get(
    "/get_verified_gym_coaches",
    status_code=status.HTTP_200_OK,
    response_model=list[UserGetVerifiedGymCoachesSchema]
)
async def user_get_verified_gym_coaches(
        request: Request,
        user_service: Annotated[UserMainService, Depends()],
        gym_id: int
):
    user_ip = request.client.host
    logger.info(f'[...] Getting Verified Gym Coaches For User {user_ip}')
    return await user_service.user_get_verified_gym_coaches(gym_id)


@user_core_router.get(
    "/get_verified_gym_plan_price",
    status_code=status.HTTP_200_OK,
    response_model=list[UserGetVerifiedGymPlanPriceSchema]
)
async def user_get_verified_gym_plan_price(
        request: Request,
        user_service: Annotated[UserMainService, Depends()],
        gym_id: int
):
    user_ip = request.client.host
    logger.info(f'[...] Getting Verified Gym Plan Price For User With IP {user_ip}')
    return await user_service.user_get_verified_gym_plan_price(gym_id)


@user_core_router.get(
    "/get_verified_gym_comments",
    status_code=status.HTTP_200_OK,
    response_model=list[UserGetVerifiedGymCommentsSchema]
)
async def user_get_verified_gym_comments(
        request: Request,
        user_service: Annotated[UserMainService, Depends()],
        gym_id: int
):
    user_ip = request.client.host
    logger.info(f'[...] Getting Verified Gym Comments For User With IP {user_ip}')
    return await user_service.user_get_verified_gym_comments(gym_id)


@user_core_router.post(
    "/gym_registration",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserGymRegistrationResponseSchema
)
async def user_gym_registration(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_gym_registration_schema: CreateUserGymRegistrationSchema,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Creating User Gym Registration for User {current_user.id}')
    return await user_service.create_user_gym_registration(current_user.id, user_gym_registration_schema)


@user_core_router.get(
    "/get_gym_registration_info",
    status_code=status.HTTP_200_OK,
    response_model=UserGetGymRegistrationsSchema
)
async def user_get_gym_registration_info(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f"[...] Getting Gym Registration Info For User {current_user.id}")
    return await user_service.get_user_gym_registration_info(current_user.id)


@user_core_router.post(
    "/create_gym_comment",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserGymCommentResponseSchema
)
async def user_gym_comment(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_gym_comment_schema: CreateUserGymCommentSchema,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Creating User Gym Comment for User {current_user.id}')
    return await user_service.create_user_gym_comment(current_user.id, user_gym_comment_schema)


# **************************************************************************
@user_core_router.get(
    "/get_verified_coach_comments",
    status_code=status.HTTP_200_OK,
    response_model=list[UserGetVerifiedCoachCommentsSchema]
)
async def user_get_verified_coach_comments(
        request: Request,
        user_service: Annotated[UserMainService, Depends()],
        coach_id: int
):
    user_ip = request.client.host
    logger.info(f'[...] Getting Verified Coach Comments For User With IP {user_ip}')
    return await user_service.user_get_verified_coach_comments(coach_id)


@user_core_router.post(
    "/create_coach_comment",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserCoachCommentResponseSchema
)
async def user_coach_comment(
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_coach_comment_schema: CreateUserCoachCommentSchema,
        user_service: Annotated[UserMainService, Depends()]
):
    logger.info(f'[...] Creating User Coach Comment for User {current_user.id}')
    return await user_service.create_user_coach_comment(current_user.id, user_coach_comment_schema)



@user_core_router.get(
    "/get_coach_plan_price",
    status_code=status.HTTP_200_OK,
    response_model=UserGetCoachPlanPriceSchema
)
async def user_get_coach_plan_price(
        user_service: Annotated[UserMainService, Depends()],
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
):
    logger.info(f"[...] Getting Coach Plan Price for User {current_user.id}")
    return await user_service.user_get_coach_plan_price(current_user.id)
