from typing import Annotated
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.domain.schemas.gym_schema import (GymRegisterSchema,
                                           GymRegisterResponseSchema,
                                           GymVerificationStatus)

from app.subservices.gym_subservice import GymSubService
from app.subservices.baseconfig import BaseService


class GymMainService(BaseService):
    def __init__(self,
                 gym_subservice: Annotated[GymSubService, Depends()]
                 ):
        super().__init__()
        self.gym_subservice = gym_subservice

    async def gym_register(self, coach_id: int, gym_register_schema: GymRegisterSchema) -> GymRegisterResponseSchema:
        new_gym = await self.gym_subservice.create_gym(coach_id, gym_register_schema)

        logger.info(f"[+] Gym With Name --> {new_gym.name} Created Successfully")

        gym_register_response = GymRegisterResponseSchema(
            message="Gym Registered Successfully Wait For Admin Verification...",
            verification_status=GymVerificationStatus.pending,
            created_at=new_gym.created_at,
            updated_at=new_gym.updated_at
        )
        return gym_register_response
