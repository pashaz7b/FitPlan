from loguru import logger
import sys
import os


def configure_logger():
    os.makedirs("FitPlan_logs", exist_ok=True)

    logger.remove()

    json_logging_format = {
        "rotation": "20 MB",
        "retention": "20 days",
        "serialize": True,
    }

    logger.add("FitPlan_logs/iam_service_info.log", level="INFO", **json_logging_format)
    logger.add("FitPlan_logs/iam_service_error.log", level="ERROR", **json_logging_format)

    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:" \
                 "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    logger.add(sys.stdout, level="INFO", format=log_format)

    logger.add(sys.stderr, level="ERROR", backtrace=True, diagnose=True, format=log_format)
