from app import schemas
from datetime import datetime

mock_books = [
    {
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
    },
    {
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
