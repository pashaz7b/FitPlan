from typing import Annotated
from fastapi import Depends

from app.subservices.user_subservice import UserSubService
from app.subservices.coach_subservice import CoachSubService
from app.infrastructure.message_broker.rabbitmq_producer import RabbitmqProducer


class SendIdToChat:
    def __init__(self,
                 rabbitmq_producer: Annotated[RabbitmqProducer, Depends()],
                 user_subservice: Annotated[UserSubService, Depends()],
                 coach_subservice: Annotated[CoachSubService, Depends()], ):
        self.user_subservice = user_subservice
        self.coach_subservice = coach_subservice
        self.rabbitmq_producer = rabbitmq_producer

    async def send_user_coach_create_id(self, user_id: int, coach_id: int):
        await self.rabbitmq_producer.send_id(user_id, coach_id, "user_coach_create")

    async def send_user_coach_change_id(self, user_id: int, coach_id: int):
        await self.rabbitmq_producer.send_id(user_id, coach_id, "user_coach_change")
