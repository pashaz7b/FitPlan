from typing import Annotated
from fastapi import Depends

from app.subservices.user_subservice import UserSubService
from app.subservices.coach_subservice import CoachSubService
from app.subservices.admin_subservice import AdminSubService
from app.infrastructure.message_broker.rabbitmq_producer import RabbitmqProducer


class SendIdToChat:
    def __init__(self,
                 rabbitmq_producer: Annotated[RabbitmqProducer, Depends()],
                 user_subservice: Annotated[UserSubService, Depends()],
                 coach_subservice: Annotated[CoachSubService, Depends()],
                 admin_subservice: Annotated[AdminSubService, Depends()]):
        self.user_subservice = user_subservice
        self.coach_subservice = coach_subservice
        self.admin_subservice = admin_subservice
        self.rabbitmq_producer = rabbitmq_producer


    async def send_user_id(self, user_email: str):
        user = await self.user_subservice.get_user_by_email(user_email)
        await self.rabbitmq_producer.send_id(user.id, "user")

    async def send_coach_id(self, coach_email: str):
        coach = await self.coach_subservice.get_coach_by_email(coach_email)
        await self.rabbitmq_producer.send_id(coach.id, "coach")

    async def send_admin_id(self, admin_email: str):
        admin = await self.admin_subservice.get_admin_by_email(admin_email)
        await self.rabbitmq_producer.send_id(admin.id, "admin")      
    