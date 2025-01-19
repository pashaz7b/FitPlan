from typing import Annotated
from fastapi import APIRouter, Depends, status
from loguru import logger

from app.domain.schemas.coach_schema import SetCoachInfoSchema
from app.domain.schemas.token_schema import TokenDataSchema
from app.domain.schemas.user_schema import SetUserInfoSchema, SetUserInfoResponseSchema
from app.mainservices.admin_auth_service import get_current_admin
from app.domain.schemas.admin_schema import (GetAdminInfoSchema,
                                             SetAdminInfoSchema, GetAdminAllUsersSchema, GetAdminAllCoachSchema,
                                             GetAdminAllTransactionSchema)

from app.mainservices.admin_mainservice import AdminMainService
from app.mainservices.coach_mainservice import CoachMainService
from app.mainservices.user_mainservice import UserMainService

admin_core_router = APIRouter()


@admin_core_router.get(
    "/get_admin_info",
    response_model=GetAdminInfoSchema,
    status_code=status.HTTP_200_OK
)
async def get_admin_info(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Get admin info for admin {current_admin.id}')
    return await admin_service.get_admin_info(current_admin.id)


@admin_core_router.put(
    "/change_admin_info",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def change_admin_info(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_data: SetAdminInfoSchema,
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Change Admin info for Admin {current_admin.id}')
    return await admin_service.change_admin_info(current_admin.id, admin_data)


@admin_core_router.get(
    "/get_all_users",
    response_model=list[GetAdminAllUsersSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_users(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Get all users for admin {current_admin.id}')
    return await admin_service.get_admin_all_users(current_admin.id)


@admin_core_router.get(
    "/get_all_coach",
    response_model=list[GetAdminAllCoachSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_coach(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Get all coach for admin {current_admin.id}')
    return await admin_service.get_admin_all_coach(current_admin.id)


@admin_core_router.get(
    "/get_all_transactions",
    response_model=list[GetAdminAllTransactionSchema],
    status_code=status.HTTP_200_OK
)
async def get_all_transactions(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminMainService, Depends()]
):
    logger.info(f'Get all transactions for admin {current_admin.id}')
    return await admin_service.get_all_transaction(current_admin.id)


@admin_core_router.put(
    "/change_user_info",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def change_user_info(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        user_data: SetUserInfoSchema,
        user_service: Annotated[UserMainService, Depends()],
        admin_service: Annotated[AdminMainService, Depends()],
        user_id: int
):
    logger.info(f'[...] Changing user info for user {user_id}')
    await admin_service.check_user_exits(user_id)
    return await user_service.change_user_info(user_id, user_data)


@admin_core_router.put(
    "/change_coach_info",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def change_coach_info(
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        set_coach_info: SetCoachInfoSchema,
        coach_service: Annotated[CoachMainService, Depends()],
        admin_service: Annotated[AdminMainService, Depends()],
        coach_id: int
):
    logger.info(f'Change coach info for coach {coach_id}')
    await admin_service.check_coach_exits(coach_id)
    return await coach_service.change_coach_info(coach_id, set_coach_info)
