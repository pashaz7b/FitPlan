from app.mainservices.connection_manager import CoachConnectionManager, UserConnectionManager
from loguru import logger

coach_connection_manager = CoachConnectionManager()
user_connection_manager = UserConnectionManager()


def get_coach_connection_manager():
    logger.info(f"Providing CoachConnectionManager instance: {id(coach_connection_manager)}")
    logger.info(f"{coach_connection_manager.active_connections}")
    return coach_connection_manager


def get_user_connection_manager():
    return user_connection_manager
