from typing import Annotated, List
from loguru import logger
from fastapi import APIRouter, Depends, UploadFile, status, File
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

from app.domain.schemas.media_schema import MediaGetSchema, MediaSchema
from app.domain.schemas.token_schema import TokenDataSchema
from app.services.media_service import MediaService
from app.services.coach_auth_service import get_current_coach
from app.services.admin_auth_service import get_current_admin
# from app.services.coach_main_service import CoachProfile
# from app.services.user_mainservice import UserProfile
from app.services.gym_mainservice import GymMainService
from app.validators.file_validator import validate_image_file
from bson import ObjectId

gym_media_router = APIRouter()


@gym_media_router.post(
    "/upload_licence_image", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_gym_licence_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
):
    logger.info("[...] Validating Image File")
    validate_image_file(file)

    logger.info(f"[+] Uploading Gym Licence Image ---> {file.filename}")
    output = await media_service.create_media(file, current_coach.email + "/Gym_licence")
    return output


@gym_media_router.post(
    "/upload_gym_image", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_gym_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
):
    logger.info("[...] Validating Image File")
    validate_image_file(file)

    logger.info(f"[+] Uploading Gym Image ---> {file.filename}")
    output = await media_service.create_media(file, current_coach.email + "/Gym")
    return output


@gym_media_router.get(
    "/download_gym_image/{gym_id}", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_gym_media(
        media_service: Annotated[MediaService, Depends()],
        gym_mainservice: Annotated[GymMainService, Depends()],
        gym_id: int
):
    # gym_response = await gym_mainservice.get_gym(gym_id)
    # logger.info(f"[+] Gym Image Retrieved ---> {gym_response}")
    # mongo_id = ObjectId(gym_response.image)
    # logger.info(f"[+] Mongo Id ---> {mongo_id}")

    gym_mongo_id = await gym_mainservice.get_gym_image(gym_id)

    media_schema, file_stream = await media_service.get_gym_media(
        gym_mongo_id
    )

    logger.info(f"Retrieving media file {media_schema.filename}")

    return StreamingResponse(
        content=file_stream(),
        media_type=media_schema.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media_schema.filename}"
        },
    )


@gym_media_router.get(
    "/download_gym_licence_image/{gym_id}", response_class=StreamingResponse, status_code=status.HTTP_200_OK
)
async def get_gym_licence_media(
        media_service: Annotated[MediaService, Depends()],
        current_admin: Annotated[TokenDataSchema, Depends(get_current_admin)],
        gym_mainservice: Annotated[GymMainService, Depends()],
        gym_id: int
):
    logger.info(f"Getting Gym {gym_id} Licence Image For Admin {current_admin.id}")

    gym_mongo_id = await gym_mainservice.get_gym_licence_image(gym_id)

    media_schema, file_stream = await media_service.get_gym_media(
        gym_mongo_id
    )

    logger.info(f"Retrieving media file {media_schema.filename}")

    return StreamingResponse(
        content=file_stream(),
        media_type=media_schema.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media_schema.filename}"
        },
    )


@gym_media_router.put(
    "/change_gym_image/{gym_id}", response_model=MediaSchema, status_code=status.HTTP_201_CREATED
)
async def upload_media(
        media_service: Annotated[MediaService, Depends()],
        file: UploadFile,
        current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
        gym_mainservice: Annotated[GymMainService, Depends()],
        gym_id: int
):
    logger.info("[...] Validating Image File")
    validate_image_file(file)

    await gym_mainservice.check_gym_owner(current_coach.id, gym_id)
    logger.info(f"[+] Uploading Media File ---> {file.filename}")
    output = await media_service.create_media(file, current_coach.email + "/Gym")
    await gym_mainservice.change_gym_image(gym_id, {"image": str(output.mongo_id)})
    return output

# *****************************************************************************************

# @gym_media_router.post(
#     "/upload_gym_images", response_model=List[MediaSchema], status_code=status.HTTP_201_CREATED
# )
# async def upload_gym_media(
#         media_service: Annotated[MediaService, Depends()],
#         files: List[UploadFile],
#         current_coach: Annotated[TokenDataSchema, Depends(get_current_coach)],
# ):
#     logger.info("[...] Validating Image Files")
#     for file in files:
#         validate_image_file(file)
#
#     logger.info(f"[+] Uploading {len(files)} Gym Images")
#     results = []
#     for file in files:
#         output = await media_service.create_media(file, current_coach.email + "/Gym")
#         results.append(output)
#     return results
