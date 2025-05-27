from fastapi.testclient import TestClient
from app.main import app
from app import services
from .test_conf import (
    mock_users,
    override_get_current_active_user_admin,
    override_get_current_active_user_user,
)

client = TestClient(app)


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
