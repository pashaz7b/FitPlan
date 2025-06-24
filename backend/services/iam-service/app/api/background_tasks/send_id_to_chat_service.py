from typing import Annotated
from fastapi import Depends
from app.subservices.user_subservice import UserSubService
from app.domain.schemas.user_schema import VerifyOTPSchema
from app.infrastructure.clients.rabbitmq_producer import RabbitmqProducer


class SendIdToChat:
    def __init__(self, user_subservice: Annotated[UserSubService, Depends()]):
        self.user_subservice = user_subservice

    async def send_user_id(self, verify_user_schema: VerifyOTPSchema):
        user = await self.user_subservice.get_user_by_email(verify_user_schema.email)
        rabbitmq_producer = RabbitmqProducer()
        await rabbitmq_producer.send_id(user.id, "user")
    