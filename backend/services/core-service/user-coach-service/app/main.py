from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.endpoints.coach_api import coach_core_router
from app.api.v1.endpoints.user_api import user_core_router
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

app.include_router(user_core_router, prefix="/api/v1/user", tags=["User"])
app.include_router(coach_core_router, prefix="/api/v1/coach", tags=["Coach"])

logger.info("User-Coach Service Started")


@app.get("/")
async def root():
    return {"Hello User-Coach Service!"}
