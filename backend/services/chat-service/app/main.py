from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from contextlib import asynccontextmanager

# from app.api.v1.endpoints.admin_api import admin_chat_router
from app.api.v1.endpoints.coach_api import coach_chat_router
from app.api.v1.endpoints.user_api import user_chat_router
from app.logging_service.logging_config import configure_logger
from app.infrastructure.message_broker.rabbitmq_consumer import RabbitmqConsumer

configure_logger()
rabbitmq_consumer = RabbitmqConsumer()

# app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start consuming
    await rabbitmq_consumer.consume_all()
    yield
    # stop consuming
    await rabbitmq_consumer.stop_consume()

app = FastAPI(lifespan=lifespan)

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
