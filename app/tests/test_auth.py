from .. import schemas


def test_user_creation(fake_session, fake_user_service, test_client):
    url = "/signup"
    signup_data = {
        "username": "bob",
        "email": "cepilep281@dlbazi.com",
        "hashed_password": "!Sup3rpassword",
    }
    response = test_client.post(
        url=url,
        json=signup_data,
    )

    user_data = schemas.UserCreate(**signup_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(
        signup_data["email"], fake_session
    )
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.user_exists_called_once_with(user_data, fake_session)
