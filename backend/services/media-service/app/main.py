from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.endpoints.admin_media_api import admin_media_router
from app.api.v1.endpoints.user_media_api import user_media_router
from app.api.v1.endpoints.coach_media_api import coach_media_router
from app.api.v1.endpoints.gym_media_api import gym_media_router
from app.logging_service.logging_config import configure_logger

configure_logger()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_media_router, prefix="/api/v1/users/media", tags=["user_media"])
app.include_router(coach_media_router, prefix="/api/v1/coach/media", tags=["coach_media"])
app.include_router(admin_media_router, prefix="/api/v1/admin/media", tags=["admin_media"])
app.include_router(gym_media_router, prefix="/api/v1/gym/media", tags=["gym_media"])

logger.info("Media Service Started")


@app.get("/")
async def root():
    return {"message": "Media Service Root"}
