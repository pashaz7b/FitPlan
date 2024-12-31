from typing import Annotated
from loguru import logger
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

from app.domain.schemas.media_schema import MediaGetSchema, MediaSchema
from app.domain.schemas.token_schema import TokenDataSchema
from app.services.media_service import MediaService
from app.services.coach_auth_service import get_current_coach
from app.services.coach_main_service import CoachProfile
from app.services.user_mainservice import UserProfile
from bson import ObjectId

coach_media_router = APIRouter()


@coach_media_router.put(
    "/change_profile", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        coach_service: Annotated[CoachProfile, Depends()],
):
    logger.info(f"[+] Uploading Coach Profile Picture ---> {file.filename}")
    output = await media_service.create_media(file, current_coach.email)
    await coach_service.change_coach_profile(current_coach.email, {"image": str(output.mongo_id)})
    return output


@coach_media_router.get(
    "/get_profile", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_media(
        media_service: Annotated[MediaService, Depends()],
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        coach_service: Annotated[CoachProfile, Depends()],
):
    user_response = await coach_service.get_coach_profile(current_coach.email)
    logger.info(f"[+] Coach Profile Picture Retrieved ---> {user_response}")
    mongo_id = ObjectId(user_response.image)
    logger.info(f"[+] Mongo Id ---> {mongo_id}")

    media_schema, file_stream = await media_service.get_media(
        mongo_id, current_coach.email
    )

    logger.info(f"Retrieving media file {media_schema.filename}")

    return StreamingResponse(
        content=file_stream(),
        media_type=media_schema.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media_schema.filename}"
        },
    )


@coach_media_router.get(
    "/get_user_profile/{user_email}", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_user_profile(
        media_service: Annotated[MediaService, Depends()],
        user_service: Annotated[UserProfile, Depends()],
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        user_email: str
):
    user_response = await user_service.get_user_profile(user_email)
    logger.info(f"[+] User Profile Retrieved ---> {user_response}")

    if not user_response:
        logger.error(f"No user found with email {user_email}")
        raise HTTPException(
            status_code=404,
            detail=f"No user found with email {user_email}"
        )

    if not user_response.image:
        raise HTTPException(
            status_code=404,
            detail="No image found for the specified user"
        )

    mongo_id = ObjectId(user_response.image)
    logger.info(f"[+] Mongo Id ---> {mongo_id}")

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
