from unittest.mock import patch
import pytest
from starlette import status

from app import services, errors
from .test_conf import (
    override_get_current_active_user_user,
    client,
    app,
    fake_user,
    fake_book_1,
)


@pytest.fixture()
def add_to_basket_response():
    return {
        "message": "Book added to basket",
        "status": status.HTTP_200_OK,
        "username": fake_user.username,
        "book_name": fake_book_1["book_name"],
        "quantity": 1,
    }


@pytest.fixture()
def update_basket_response():
    return {
        "message": "Quantity updated",
        "status": status.HTTP_200_OK,
        "username": fake_user.username,
        "book_name": fake_book_1["book_name"],
        "quantity": 3,
    }


@pytest.fixture()
def delete_basket_response():
    return {
        "message": "Book removed from basket",
        "status": status.HTTP_200_OK,
        "username": fake_user.username,
        "book_name": fake_book_1["book_name"],
    }


def test_get_users_me_basket_unauthorized():
    response = client.get("/users/me/basket")
    assert response.status_code == 401


def test_get_users_me_basket_authorized():
    mock_basket = [
        {"book": fake_book_1, "quantity": 1, "user_id": fake_user.user_id},
    ]

    with patch("app.services.get_basket", return_value=mock_basket):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )

        response = client.get("/users/me/basket")

        assert response.status_code == 200
        assert response.json()[0]["book"]["book_name"] == fake_book_1["book_name"]
        app.dependency_overrides.clear()


def test_post_users_me_basket_unauthorized():
    response = client.post("/users/me/basket")
    assert response.status_code == 401


def test_post_users_me_basket_authorized_valid(add_to_basket_response):
    with patch("app.services.add_to_basket", return_value=add_to_basket_response):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )

        response = client.post(f"/users/me/basket?book_id={fake_book_1['book_id']}")
        assert response.status_code == 200
        assert response.json()["book_name"] == fake_book_1["book_name"]
        app.dependency_overrides.clear()


def test_put_users_me_basket_unauthorized():
    response = client.put("/users/me/basket?book_id=1", json={"quantity": 3})
    assert response.status_code == 401


def test_put_users_me_basket_authorized_valid(update_basket_response):
    with patch(
        "app.services.update_basket_quantity", return_value=update_basket_response
    ):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )

        response = client.put(
            f"/users/me/basket?book_id={fake_book_1['book_id']}",
            json={"quantity": 3},
        )

        assert response.status_code == 200
        assert response.json()["quantity"] == 3
        assert response.json()["book_name"] == fake_book_1["book_name"]
        app.dependency_overrides.clear()


def test_delete_users_me_basket_unauthorized():
    response = client.delete("/users/me/basket?book_id=1")
    assert response.status_code == 401


def test_delete_users_me_basket_authorized_valid(delete_basket_response):
    with patch("app.services.delete_from_basket", return_value=delete_basket_response):
        app.dependency_overrides[services.get_current_active_user] = (
            override_get_current_active_user_user
        )

        response = client.delete(f"/users/me/basket?book_id={fake_book_1['book_id']}")
        assert response.status_code == 200
        assert response.json()["message"] == "Book removed from basket"
        app.dependency_overrides.clear()
