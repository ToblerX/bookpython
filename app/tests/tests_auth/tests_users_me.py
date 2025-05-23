from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app import schemas, services

client = TestClient(app)


# Override dependency for non-admin user
def override_get_current_active_user():
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


def test_get_users_me_unauthorized():
    response = client.get("/users/me")

    assert response.status_code == 401


def test_get_users_me_authorized():
    app.dependency_overrides[services.get_current_active_user] = (
        override_get_current_active_user
    )

    response = client.get("/users/me")

    assert response.status_code == 200
    assert response.json()["username"] == "user"

    app.dependency_overrides.clear()
