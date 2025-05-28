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

fake_book_1 = {
    "book_id": 1,
    "book_name": "The AI Revolution",
    "book_author": "Jane Smith",
    "book_description": "An insightful look into the rise of artificial intelligence.",
    "book_price": 29.99,
    "supply": 50,
    "book_cover_path": "app/static/images/books/cover_not_available.jpg",
    "genres": [],
    "created_at": datetime(2025, 5, 1, 10, 30),
    "updated_at": datetime(2025, 5, 10, 15, 45),
}
fake_book_2 = {
    "book_id": 2,
    "book_name": "Mysteries of the Orient",
    "book_author": "John Doe",
    "book_description": "A thrilling mystery novel set aboard the legendary Orient Express.",
    "book_price": 19.99,
    "supply": 30,
    "book_cover_path": "app/static/images/books/cover_not_available.jpg",
    "genres": [],
    "created_at": datetime(2025, 4, 20, 9, 15),
    "updated_at": datetime(2025, 5, 5, 11, 0),
}
# Mock books to return from the endpoint
mock_books = [
    fake_book_1,
    fake_book_2,
]

fake_admin = schemas.UserModel(
    user_id=0,
    username="admin",
    email="admin@gmail.com",
    disabled=False,
    verified=True,
    role="admin",
    created_at=datetime.now(),
    updated_at=datetime.now(),
)

fake_user = schemas.UserModel(
    user_id=10,
    username="user",
    email="user@example.com",
    disabled=False,
    verified=True,
    role="user",
    created_at=datetime.now(),
    updated_at=datetime.now(),
)


# Override dependency for admin user
def override_get_current_active_user_admin():
    return fake_admin


# Override dependency for non-admin user
def override_get_current_active_user_user():
    return fake_user
