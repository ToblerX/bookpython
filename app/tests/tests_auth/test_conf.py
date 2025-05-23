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
