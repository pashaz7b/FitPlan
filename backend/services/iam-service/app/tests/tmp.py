import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status
from uuid import uuid4

from app.main import app


async def get_mock_user():
    """Generate mock user data."""
    return {
        "user_name": f"user_{uuid4().hex[:8]}_{uuid4().int % 10000}",
        "name": "Test User",
        "email": f"{uuid4().hex[:8]}_{uuid4().int % 10000}@example.com",
        "password": "Test@1234",
        "phone_number": f"{uuid4().int % 10000000000}",
        "gender": "Male",
        "date_of_birth": "1990-01-01",
        "height": 170.5,
        "weight": 70.0
    }


@pytest_asyncio.fixture(autouse=True)
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_user_signup(client):
    """Test user signup functionality."""
    mock_user = await get_mock_user()

    # Initial signup
    response = await client.post("/api/v1/users/signup", json=mock_user)
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()

    assert "id" in response_data
    assert response_data["email"] == mock_user["email"]
    assert response_data["is_verified"] is False
    assert "message" in response_data
    assert response_data["message"].startswith("User Created Successfully")

    # Attempting signup with the same email should fail
    response = await client.post("/api/v1/users/signup", json=mock_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "User With This Email Already Exists"


@pytest.mark.asyncio
async def test_verify_otp(client):
    """Test OTP verification functionality."""
    mock_user = await get_mock_user()

    # Signup user
    signup_response = await client.post("/api/v1/users/signup", json=mock_user)
    assert signup_response.status_code == status.HTTP_201_CREATED
    signup_data = signup_response.json()

    otp = input("Enter OTP: ")
    # Mock OTP verification request
    verify_otp_data = {
        "email": mock_user["email"],
        "OTP": otp
    }

    # Verify OTP
    response = await client.post("/api/v1/users/verifyOTP", json=verify_otp_data)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "verified" in response_data
    assert response_data["verified"] is True
    assert "message" in response_data
    assert response_data["message"] == "User Verified Successfully"

    # Attempt with invalid OTP
    invalid_otp_data = {
        "email": mock_user["email"],
        "OTP": "6543210"  # Invalid OTP
    }
    response = await client.post("/api/v1/users/verifyOTP", json=invalid_otp_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()

    assert "detail" in response_data
    assert response_data["detail"] == "Invalid OTP"
