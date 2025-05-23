import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


@pytest.fixture
def user_data():
    return {
        "username": "testuser1",
        "email": "test@example.com",
        "hashed_password": "1!SecurePass",
    }


def test_signup_success(user_data):
    with (
        patch("app.services.user_exists", return_value=False),
        patch("app.services.email_exists", return_value=False),
        patch("app.services.create_user", return_value={"email": user_data["email"]}),
        patch("app.services.send_verification_email") as mock_send,
    ):

        response = client.post("/signup", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert (
            data["message"]
            == "Account created, check your email to verify your account"
        )
        assert data["user"]["email"] == user_data["email"]
        mock_send.assert_called_once_with(user_data["email"])


def test_signup_duplicate_username(user_data):
    with (
        patch("app.services.user_exists", return_value=True),
        patch("app.services.email_exists"),
        patch("app.services.send_verification_email"),
    ):

        response = client.post("/signup", json=user_data)
        assert response.status_code == 403
        assert "User account already exists." in response.text


def test_signup_duplicate_email(user_data):
    with (
        patch("app.services.user_exists", return_value=False),
        patch("app.services.email_exists", return_value=True),
        patch("app.services.send_verification_email"),
    ):

        response = client.post("/signup", json=user_data)
        assert response.status_code == 403
        assert "Email account already exists." in response.text
