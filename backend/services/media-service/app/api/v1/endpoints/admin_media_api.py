from typing import Annotated
from loguru import logger
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

from app.domain.schemas.media_schema import MediaGetSchema, MediaSchema
from app.domain.schemas.token_schema import TokenDataSchema
from app.services.media_service import MediaService
from app.services.admin_auth_service import get_current_admin
from app.services.admin_mainservice import AdminProfile
from app.services.user_mainservice import UserProfile
from app.services.coach_main_service import CoachProfile
from app.validators.file_validator import validate_image_file
from bson import ObjectId

admin_media_router = APIRouter()


@admin_media_router.put(
    "/change_profile", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminProfile, Depends()],
):
    logger.info("[...] Validating Image File")
    validate_image_file(file)

    logger.info(f"[+] Uploading Admin Profile Picture ---> {file.filename}")
    output = await media_service.create_media(file, current_admin.email)
    await admin_service.change_admin_profile(current_admin.email, {"image": str(output.mongo_id)})
    return output


@admin_media_router.get(
    "/get_profile", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_media(
        media_service: Annotated[MediaService, Depends()],
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminProfile, Depends()],
):
    admin_response = await admin_service.get_admin_profile(current_admin.email)
    logger.info(f"[+] Admin Profile Picture Retrieved ---> {admin_response}")
    mongo_id = ObjectId(admin_response.image)
    logger.info(f"[+] Mongo Id ---> {mongo_id}")

    media_schema, file_stream = await media_service.get_media(
        mongo_id, admin_response.email
    )

    logger.info(f"Retrieving media file {media_schema.filename}")

    return StreamingResponse(
        content=file_stream(),
        media_type=media_schema.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media_schema.filename}"
        },
    )


@admin_media_router.get(
    "/get_user_profile/{user_email}", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_user_profile(
        media_service: Annotated[MediaService, Depends()],
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminProfile, Depends()],
        user_email: str
):
    logger.info(f"[+] Fetching User For Admin With Email ---> {current_admin.email}")

    mongo_id = await admin_service.admin_get_user_profile(user_email)

    media_schema, file_stream = await media_service.get_media(
        mongo_id, user_email
    )

    logger.info(f"Retrieving media file {media_schema.filename}")

    return StreamingResponse(
        content=file_stream(),
        media_type=media_schema.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media_schema.filename}"
        },
    )


@admin_media_router.get(
    "/get_coach_profile/{coach_email}", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_coach_profile(
        media_service: Annotated[MediaService, Depends()],
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminProfile, Depends()],
        coach_email: str
):
    logger.info(f"[+] Fetching Coach For Admin With Email ---> {current_admin.email}")

    mongo_id = await admin_service.admin_get_coach_profile(coach_email)

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


@admin_media_router.put(
    "/change_user_profile", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_user_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        admin_service: Annotated[AdminProfile, Depends()],
        user_service: Annotated[UserProfile, Depends()],
        user_email: str
):
    logger.info("[...] Validating Image File")
    validate_image_file(file)

    await admin_service.admin_check_user(user_email)
    logger.info(f"[+] Uploading Media File ---> {file.filename}")
    output = await media_service.create_media(file, user_email)
    await user_service.change_profile(user_email, {"image": str(output.mongo_id)})
    return output


@admin_media_router.put(
    "/change_coach_profile", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_coach_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        coach_service: Annotated[CoachProfile, Depends()],
        admin_service: Annotated[AdminProfile, Depends()],
        coach_email: str
):
    logger.info("[...] Validating Image File")
    validate_image_file(file)

    await admin_service.admin_check_coach(coach_email)
    logger.info(f"[+] Uploading Coach Profile Picture ---> {file.filename}")
    output = await media_service.create_media(file, coach_email)
    await coach_service.change_coach_profile(coach_email, {"image": str(output.mongo_id)})
    return output
