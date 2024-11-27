import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from fastapi import status

from app.main import app

@pytest_asyncio.fixture(autouse=True)
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

async def get_mock_email():
    from uuid import uuid4
    return f"{uuid4()}@example.com"

@pytest.mark.asyncio
@patch("app.subservices.auth.otp_subservice.OTPSubservice.send_otp", new_callable=AsyncMock)
async def test_coach_register(mock_send_otp, client):
    # Mock the OTP service
    mock_send_otp.return_value = "123456"

    email = await get_mock_email()
    payload = {
        "user_name": "test_user",
        "name": "Test Coach",
        "email": email,
        "phone_number": "1234567890",
        "password": "StrongP@ssw0rd",
        "gender": "male",
        "date_of_birth": "1350/11/01",
        "height": 180,
        "weight": 80,
        "specialization": "aaa",
        "biography": "bbb"
    }

    # First registration
    response = await client.post("/api/v1/coach/signup/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "id" in response_data
    assert response_data["email"] == email
    assert response_data["message"] == "[+] Coach Created Successfully, OTP Sent To The Email"

    # Duplicate registration
    response = await client.post("/api/v1/coach/signup/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Coach with this email already exists."
