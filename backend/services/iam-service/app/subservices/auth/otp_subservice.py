import random
from typing import Annotated
from loguru import logger
from fastapi import Depends
from passlib.handlers.django import django_disabled
from redis import Redis

from app.core.redis.redis_database import get_redis_client
from app.subservices.baseconfig import BaseService

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class OTPSubservice(BaseService):
    def __init__(self, redis_client: Annotated[Redis, Depends(get_redis_client)]) -> None:
        super().__init__()
        self.redis_client = redis_client

    def send_email(self, email: str, otp: str):
        try:
            message = MIMEMultipart()
            message["From"] = self.config.EMAIL_FROM
            message["To"] = email
            message["Subject"] = "Your OTP Code"
            body = f"Your OTP code is: {otp}"
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL(self.config.SMTP_SERVER, self.config.SMTP_PORT) as server:
                server.login(self.config.SMTP_USERNAME, self.config.SMTP_PASSWORD)
                server.sendmail(self.config.EMAIL_FROM, email, message.as_string())

            logger.info(f"[+] OTP {otp} Sent To Email {email}")
        except Exception as e:
            logger.error(f"Failed To Send Email: {e}")

    def send_sms_to_phone_number(self, phone_number: str, otp: str):
        pass

    @staticmethod
    def __generate_otp() -> str:
        return str(random.randint(10000, 99999))

    def send_otp(self, email: str):
        otp = self.__generate_otp()
        self.redis_client.setex(email, self.config.OTP_EXPIRE_TIME, otp)
        try:
            self.send_email(email, otp)
        except Exception as e:
            logger.error(f"Failed Sending OTP To email: {e}")
        logger.info(f"OTP {otp} sent to email {email}")
        return otp

    def verify_otp(self, email: str, otp: str) -> bool:
        stored_otp = self.redis_client.get(email)
        return stored_otp is not None and stored_otp == otp

    def check_exist(self, email: str) -> bool:
        stored_otp = self.redis_client.get(email)
        return stored_otp is not None

    # *********************************************************************************
    def send_otp_to_phone(self, phone_number: str):
        otp = self.__generate_otp()
        self.redis_client.setex(phone_number, self.config.OTP_EXPIRE_TIME, otp)
        # self.send_sms_to_phone_number()
        logger.info(f"OTP {otp} sent to phone_number {phone_number}")
        return otp

    def verify_otp_phone(self, phone_number: str, otp: str) -> bool:
        stored_otp = self.redis_client.get(phone_number)
        return stored_otp is not None and stored_otp == otp

    def check_exist_phone(self, phone_number: str) -> bool:
        stored_otp = self.redis_client.get(phone_number)
        return stored_otp is not None
