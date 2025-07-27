# from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# from app.api.v1.endpoints.admin_api import admin_chat_router
from app.api.v1.endpoints.coach_api import coach_chat_router
from app.api.v1.endpoints.user_api import user_chat_router
from app.logging_service.logging_config import configure_logger

configure_logger()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_chat_router, prefix="/api/v1/user", tags=["User"])
app.include_router(coach_chat_router, prefix="/api/v1/coach", tags=["Coach"])
# app.include_router(admin_chat_router, prefix="/api/v1/admin", tags=["Admin"])

logger.info("Chat Service Started")


@app.get("/")
async def root():
    return {"Hello Chat Service!"}
