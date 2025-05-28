import jwt
import datetime
from fastapi import HTTPException, status, Depends, Request


class CoachOtpToken:
    def __init__(self):
        self.SECRET_KEY = "c05267002bef279fbba23202264af9a2ea4272c997ad5cda4d8aabd82f5539a2"
        self.ALGORITHM = "HS256"
        self.TOKEN_EXPIRY_MINUTES = 30

    async def create_coach_otp_token(self, phone_number: str, verified: bool) -> str:
        payload = {
            "phone_number": phone_number,
            "verified": verified,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.TOKEN_EXPIRY_MINUTES)
        }

        try:
            otp_token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
            return otp_token
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create OTP token: {str(e)}"
            )

    async def verify_coach_otp_token(self, phone_number: str, otp_token: str) -> bool:
        try:
            payload = jwt.decode(otp_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            if payload.get("phone_number") != phone_number:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token does not match the provided phone number"
                )
            if not payload.get("verified"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token is not verified"
                )

            return True

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="OTP token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP token"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to verify OTP token: {str(e)}"
            )

    @staticmethod
    async def get_otp_token(request: Request):
        otp_token = request.cookies.get("otp_token")
        if not otp_token:
            raise HTTPException(status_code=401, detail="OTP token missing")
        return otp_token
