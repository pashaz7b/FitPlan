from sys import prefix

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.endpoints.admin_api import admin_router
from app.api.v1.endpoints.coach_api import coach_router
from app.api.v1.endpoints.user_api import user_router
from app.api.v1.endpoints.gym_api import gym_router
from app.core.postgres.postgres_database import init_db
from app.loggerconfig.loggin_confs import configure_logger

configure_logger()
init_db()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(coach_router, prefix="/api/v1/coach", tags=["coach"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])

app.include_router(gym_router, prefix="/api/v1/gym", tags=["gym"])


@app.get("/")
async def root():
    message = {"Hello From IAM"}
    return message
