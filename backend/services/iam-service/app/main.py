from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.core.postgres.postgres_database import init_db
from app.api.v1.endpoints.user_api import user_router

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

@app.get("/")
async def root():
    message = {"hello my friend"}
    return message
