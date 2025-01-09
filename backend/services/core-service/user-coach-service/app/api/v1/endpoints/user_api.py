from typing import Annotated
from fastapi import APIRouter, Depends, status, Form
from loguru import logger

from app.domain.schemas.token_schema import TokenDataSchema
from app.mainservices.auth_service import get_current_user
from app.domain.schemas.user_schema import (GetUserInfoSchema,
                                            SetUserInfoSchema,
                                            GetUserTransactionsSchema)

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
    changes = user_data
    if not changes:
        return {"message": "No changes detected"}

    await user_service.change_user_info(current_user.id, changes)
    return {"message": "User information updated successfully"}


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