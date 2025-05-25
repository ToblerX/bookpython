from datetime import datetime

from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from .test_conf import (
    mock_books,
    override_get_current_active_user_admin,
    override_get_current_active_user_user,
)
import pytest

from ... import services

client = TestClient(app)


@pytest.fixture
def book_data():
    return {
        "book_name": "book1",
        "book_author": "bob bob",
        "book_description": "This is a book." * 10,
        "book_price": 100,
        "supply": 100,
    }


created_from_book_data = {
    "book_id": 1,
    "book_name": "Book1",
    "book_author": "bob bob",
    "book_description": "This is a book." * 10,
    "book_price": 100.0,
    "supply": 100,
    "book_cover_path": "app/static/images/books/cover_not_available.jpg",
    "genres": [],
    "created_at": datetime(2025, 5, 20, 10, 0),
    "updated_at": datetime(2025, 5, 21, 15, 30),
}


def test_book_create_unauthorized():
    response = client.post("/books", json={})

    assert response.status_code == 401


def test_book_create_success(book_data):
    with patch("app.services.create_book", return_value=created_from_book_data):

        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_admin
        )

        response = client.post("/books", json=book_data)

        assert response.status_code == 200
        data = response.json()
        assert data["book_name"] == "Book1"

        app.dependency_overrides.clear()


def test_book_create_not_admin(book_data):
    app.dependency_overrides[services.get_current_active_user] = (
        override_get_current_active_user_user
    )

    response = client.post("/books", json=book_data)

    assert response.status_code == 403
    assert response.json() == {
        "message": "Only administrators can access this page.",
        "error_code": "only_admin_allowed",
    }

    app.dependency_overrides.clear()


def test_book_create_unprocessable(book_data):
    app.dependency_overrides[services.get_current_active_user] = (
        override_get_current_active_user_admin
    )

    response = client.post("/books", json={})

    assert response.status_code == 422
