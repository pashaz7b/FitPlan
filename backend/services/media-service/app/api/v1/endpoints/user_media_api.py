from fastapi import HTTPException
from typing import Annotated
from loguru import logger
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import StreamingResponse

from app.domain.schemas.media_schema import MediaGetSchema, MediaSchema
from app.domain.schemas.token_schema import TokenDataSchema
from app.services.media_service import MediaService
from app.services.auth_service import get_current_user
from app.services.user_mainservice import UserProfile
from app.services.coach_main_service import CoachProfile
from bson import ObjectId

user_media_router = APIRouter()


# @media_router.post(
#     "/UploadMedia", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
# )
# async def upload_media(
#     media_service: Annotated[MediaService, Depends()],
#     file: UploadFile,
#     current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
# ):
#     logger.info(f"Uploading media file {file.filename}")
#     return await media_service.create_media(file, current_user.id)


@user_media_router.put(
    "/change_profile", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserProfile, Depends()],
):
    logger.info(f"[+] Uploading Media File ---> {file.filename}")
    output = await media_service.create_media(file, current_user.email)
    await user_service.change_profile(current_user.email, {"image": str(output.mongo_id)})
    return output


@user_media_router.get(
    "/get_profile", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_media(
        media_service: Annotated[MediaService, Depends()],
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        user_service: Annotated[UserProfile, Depends()],
):
    user_response = await user_service.get_user_profile(current_user.email)
    logger.info(f"[+] User Profile Retrieved ---> {user_response}")
    mongo_id = ObjectId(user_response.image)
    logger.info(f"[+] Mongo Id ---> {mongo_id}")

    media_schema, file_stream = await media_service.get_media(
        mongo_id, current_user.email
    )

    logger.info(f"Retrieving media file {media_schema.filename}")

    return StreamingResponse(
        content=file_stream(),
        media_type=media_schema.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media_schema.filename}"
        },
    )


@user_media_router.get(
    "/get_coach_profile/{coach_email}", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_coach_profile(
        media_service: Annotated[MediaService, Depends()],
        coach_service: Annotated[CoachProfile, Depends()],
        current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
        coach_email: str
):
    coach_response = await coach_service.get_coach_profile(coach_email)
    logger.info(f"[+] Coach Profile Retrieved ---> {coach_response}")

    if not coach_response:
        logger.error(f"No coach found with email {coach_email}")
        raise HTTPException(
            status_code=404,
            detail=f"No coach found with email {coach_email}"
        )

    logger.info(f"[+] Coach Profile Retrieved ---> {coach_response}")

    if not coach_response.image:
        raise HTTPException(
            status_code=404,
            detail="No image found for the specified coach"
        )

    mongo_id = ObjectId(coach_response.image)
    logger.info(f"[+] Mongo Id ---> {mongo_id}")

    media_schema, file_stream = await media_service.get_media(
        mongo_id, coach_email
    )

    logger.info(f"Retrieving media file {media_schema.filename}")

    return StreamingResponse(
        content=file_stream(),
        media_type=media_schema.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media_schema.filename}"
        },
    )

# @media_router.post(
#     "/send_meal_media", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
# )
# async def upload_media(
#         media_service: Annotated[MediaService, Depends()],
#         file: UploadFile,
#         current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
#         user_service: Annotated[UserProfile, Depends()],
# ):
#     logger.info(f"[+] Uploading Meal Media File ---> {file.filename}")
#     output = await media_service.create_media(file, current_user.email)
#     await user_service.change_profile(current_user.email, {"image": str(output.mongo_id)})
#     return output


# @media_router.post(
#     "/GetMedia", response_class=StreamingResponse, status_code=status.HTTP_200_OK
# )
# async def get_media(
#     media_get: MediaGetSchema,
#     media_service: Annotated[MediaService, Depends()],
#     current_user: Annotated[TokenDataSchema, Depends(get_current_user)],
# ):
#     media_schema, file_stream = await media_service.get_media(
#         media_get.mongo_id, current_user.email
#     )
#
#     logger.info(f"Retrieving media file {media_schema.filename}")
#
#     return StreamingResponse(
#         content=file_stream(),
#         media_type=media_schema.content_type,
#         headers={
#             "Content-Disposition": f"attachment; filename={media_schema.filename}"
#         },
#     )
