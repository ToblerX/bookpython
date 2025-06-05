from unittest.mock import patch

import pytest
from starlette import status

from app import services
from ...exceptions import errors
from .test_conf import (
    override_get_current_active_user_user,
    client,
    app,
    mock_books,
    fake_user,
    fake_book_1,
)


@pytest.fixture()
def add_to_wishlist_response():
    return {
        "message": "Book added to wishlist",
        "status": status.HTTP_200_OK,
        "username": fake_user.username,
        "book_name": fake_book_1["book_name"],
    }


def test_get_users_me_wishlist_unauthorized():
    response = client.get("/users/me/wishlist")

    assert response.status_code == 401


def test_get_users_me_wishlist_authorized():
    with patch("app.services.get_wishlist", return_value=mock_books):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )

        response = client.get("/users/me/wishlist")

        assert response.status_code == 200
        assert response.json()[0]["book_name"] == "The AI Revolution"
        assert response.json()[1]["book_name"] == "Mysteries of the Orient"

        app.dependency_overrides.clear()


def test_post_users_me_wishlist_unauthorized():
    response = client.post("/users/me/wishlist")
    assert response.status_code == 401


def test_post_users_me_wishlist_authorized_valid(add_to_wishlist_response):
    with patch(
        "app.services.add_to_wishlist",
        return_value=add_to_wishlist_response,
    ):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )
        response = client.post(f"/users/me/wishlist?book_id={fake_book_1['book_id']}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["book_name"] == fake_book_1["book_name"]
        assert response.json()["username"] == fake_user.username
        app.dependency_overrides.clear()


def test_delete_users_me_wishlist_unauthorized():
    response = client.delete(f"/users/me/wishlist?book_id=1")
    assert response.status_code == 401


def test_delete_users_me_wishlist_authorized_valid():
    delete_response = {
        "message": "Book removed from wishlist.",
        "status": status.HTTP_200_OK,
        "username": fake_user.username,
        "book_name": fake_book_1["book_name"],
    }

    with patch("app.services.delete_from_wishlist", return_value=delete_response):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )

        response = client.delete(f"/users/me/wishlist?book_id={fake_book_1['book_id']}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["book_name"] == fake_book_1["book_name"]
        assert response.json()["username"] == fake_user.username
        assert response.json()["message"] == "Book removed from wishlist."

        app.dependency_overrides.clear()


def test_delete_users_me_wishlist_book_not_associated():
    with patch(
        "app.services.delete_from_wishlist", return_value=errors.BookNotAssociated
    ):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )

        response = client.delete(f"/users/me/wishlist?book_id=999")
        assert "The book is not in the wishlist." in response.text

        app.dependency_overrides.clear()
