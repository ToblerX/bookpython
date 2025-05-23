from fastapi.testclient import TestClient
from app.main import app
from app import services
from .test_conf import override_get_current_active_user_user

client = TestClient(app)


def test_get_users_me_unauthorized():
    response = client.get("/users/me")

    assert response.status_code == 401


def test_get_users_me_authorized():
    app.dependency_overrides[services.get_current_active_user] = (
        override_get_current_active_user_user
    )

    response = client.get("/users/me")

    assert response.status_code == 200
    assert response.json()["username"] == "user"

    app.dependency_overrides.clear()
