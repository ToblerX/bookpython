from unittest.mock import patch

from app import services
from .test_conf import override_get_current_active_user_user, client, app, mock_books


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
