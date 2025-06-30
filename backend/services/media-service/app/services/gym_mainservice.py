from typing import Annotated
from loguru import logger
from fastapi import Depends
from fastapi import HTTPException
from bson import ObjectId

from app.subservice.gym_subservice import GymSubService


class GymMainService():
    def __init__(self, gym_subservice: Annotated[GymSubService, Depends()]
                 ) -> None:
        super().__init__()
        self.gym_subservice = gym_subservice

    async def get_gym_image(self, gym_id: int):
        logger.info(f"Retrieving Gym Id {gym_id}")
        gym = await self.gym_subservice.get_gym(gym_id)

        if not gym:
            logger.error(f"No Gym Found With Id {gym_id}")
            raise HTTPException(status_code=404, detail="Gym Not Found")

        gym_mongo_id = ObjectId(gym.image)
        return gym_mongo_id

    async def get_gym_licence_image(self, gym_id: int):
        logger.info(f"Retrieving Gym Id {gym_id}")
        gym = await self.gym_subservice.get_gym(gym_id)

        if not gym:
            logger.error(f"No Gym Found With Id {gym_id}")
            raise HTTPException(status_code=404, detail="Gym Not Found")

        gym_mongo_id = ObjectId(gym.license_image)
        return gym_mongo_id

    async def change_gym_image(self, gym_id: int, update_fields: dict):
        logger.info(f"Updating Gym With Id {gym_id}")
        return await self.gym_subservice.update_gym(gym_id, update_fields)

    async def check_gym_owner(self, coach_id: int ,gym_id: int):
        logger.info(f"Retrieving Gym Id {gym_id}")
        gym = await self.gym_subservice.get_gym(gym_id)

        if not gym:
            logger.error(f"No Gym Found With Id {gym_id}")
            raise HTTPException(status_code=404, detail="Gym Not Found")

        gym = await self.gym_subservice.get_gym(gym_id)

        if not coach_id == gym.owner_id:
            logger.info("You Dont Have Permission To Change Gym Image")
            raise HTTPException(status_code=403, detail="Dont Have Permission To Change Gym Image")

        return True