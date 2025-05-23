from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app import schemas, services

client = TestClient(app)

# Mock users to return from the endpoint
mock_users = [
    {
        "user_id": 1,
        "username": "user1",
        "email": "user1@example.com",
        "disabled": False,
        "verified": True,
        "role": "user",
        "created_at": datetime(2024, 1, 1, 12, 0, 0),
        "updated_at": datetime(2024, 1, 2, 12, 0, 0),
    },
    {
        "user_id": 2,
        "username": "user2",
        "email": "user2@example.com",
        "disabled": False,
        "verified": True,
        "role": "admin",
        "created_at": datetime(2024, 1, 3, 12, 0, 0),
        "updated_at": datetime(2024, 1, 4, 12, 0, 0),
    },
]


# Override dependency for admin user
def override_get_current_active_user_admin():
    return schemas.UserModel(
        user_id=0,
        username="admin",
        email="admin@gmail.com",
        disabled=False,
        verified=True,
        role="admin",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


# Override dependency for non-admin user
def override_get_current_active_user_user():
    return schemas.UserModel(
        user_id=10,
        username="user",
        email="user@example.com",
        disabled=False,
        verified=True,
        role="user",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_get_users_unauthorized():
    response = client.get("/users")

    assert response.status_code == 401


def test_get_users_as_admin():
    app.dependency_overrides[services.get_current_active_user] = (
        override_get_current_active_user_admin
    )

    from unittest.mock import patch

    with patch("app.services.get_users", return_value=mock_users):
        response = client.get("/users")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["username"] == "user1"

    app.dependency_overrides.clear()


def test_get_users_as_non_admin():
    app.dependency_overrides[services.get_current_active_user] = (
        override_get_current_active_user_user
    )

    response = client.get("/users")

    assert response.status_code == 403
    assert "Only administrators can access this page." in response.text

    app.dependency_overrides.clear()
