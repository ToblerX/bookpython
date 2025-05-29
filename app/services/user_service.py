import logging
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated

from starlette import status
from starlette.responses import JSONResponse

from .. import schemas, config, mail, errors
from .. import db as app_db
import jwt


def get_password_hash(password):
    return config.PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    return config.PWD_CONTEXT.verify(plain_password, hashed_password)


def create_user(user: schemas.UserCreate, current_session: Session):
    new_user = app_db.User(**user.dict())
    new_user.hashed_password = get_password_hash(user.hashed_password)
    current_session.add(new_user)
    current_session.commit()
    current_session.refresh(new_user)
    return new_user


def user_exists(user: schemas.UserCreate, current_session: Session):
    check_user = (
        current_session.query(app_db.User)
        .filter(app_db.User.username == user.username)
        .first()
    )
    return True if check_user else False


def email_exists(user: schemas.UserCreate, current_session: Session):
    check_user = (
        current_session.query(app_db.User)
        .filter(app_db.User.email == user.email)
        .first()
    )
    return True if check_user else False


def get_users(current_session: Session):
    return current_session.query(app_db.User).all()


def get_user_by_email(email: EmailStr, current_session: Session):
    check_user = (
        current_session.query(app_db.User).filter(app_db.User.email == email).first()
    )
    if not check_user:
        raise errors.UserNotFound()
    return check_user


def update_user(user: app_db.User, user_data: dict, current_session: Session):
    for k, v in user_data.items():
        setattr(user, k, v)
    current_session.commit()
    current_session.refresh(user)
    return user


# == AUTH ==
def get_user(username: str, current_session: Session):
    user_dict = (
        current_session.query(app_db.User)
        .filter(app_db.User.username == username)
        .first()
    )
    if user_dict:
        return user_dict
    raise errors.UserNotFound()


def authenticate_user(username: str, password: str, current_session: Session):
    user = get_user(username, current_session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(config.oauth2_scheme)],
    current_session: Session = Depends(app_db.database.get_db),
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise errors.WrongCredentials()
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise errors.WrongCredentials()
    user = get_user(token_data.username, current_session)
    if user is None:
        raise errors.WrongCredentials()
    return user


def get_current_active_user(
    current_user: Annotated[schemas.UserModel, Depends(get_current_user)],
):
    if current_user.disabled:
        raise errors.UserNotActive()
    return current_user


def create_url_safe_token(data: dict):
    token = config.serializer.dumps(data)
    return token


def decode_url_safe_token(token: str):
    try:
        token_data = config.serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))
        raise errors.InvalidToken()


async def send_verification_email(user_email: EmailStr):
    token = create_url_safe_token(data={"email": user_email})

    link = f"http://{config.DOMAIN}/verify/{token}"

    html_message = f"""
        <h1>Verify your email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
        """

    message = mail.create_message(
        recipients=[user_email],
        subject="Welcome",
        body=html_message,
    )

    await mail.mail_engine.send_message(message)

    return {"status": "Email sent successfully"}


async def send_password_reset_email(user_email: EmailStr):
    token = create_url_safe_token(data={"email": user_email})

    link = f"http://{config.DOMAIN}/password-reset-confirm/{token}"

    html_message = f"""
            <h1>Reset your password</h1>
            <p>Please click this <a href="{link}">link</a> to reset your password</p>
            """

    message = mail.create_message(
        recipients=[user_email],
        subject="Reset your password",
        body=html_message,
    )

    await mail.mail_engine.send_message(message)

    return {"status": "Email sent successfully"}


def add_to_wishlist(user_id: int, book_id: int, current_session: Session):
    user = current_session.query(app_db.User).get(user_id)
    if not user:
        raise errors.UserNotFound()
    book = current_session.query(app_db.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    stmt_check = select(app_db.models.user_books_wishlist).where(
        app_db.models.user_books_wishlist.c.book_id == book_id,
        app_db.models.user_books_wishlist.c.user_id == user_id,
    )
    result = current_session.execute(stmt_check).first()
    if result:
        raise errors.BookAlreadyAssociated
    stmt = app_db.models.user_books_wishlist.insert().values(
        book_id=book_id, user_id=user_id
    )
    current_session.execute(stmt)
    current_session.commit()
    return JSONResponse(
        {
            "message": "Book added to wishlist",
            "status": status.HTTP_200_OK,
            "username": user.username,
            "book_name": book.book_name,
        }
    )


def delete_from_wishlist(user_id: int, book_id: int, current_session: Session):
    user = current_session.query(app_db.User).get(user_id)
    if not user:
        raise errors.UserNotFound()
    book = current_session.query(app_db.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    if book in user.wishlist:
        user.wishlist.remove(book)
        current_session.commit()
        return JSONResponse(
            {
                "message": "Book removed from wishlist.",
                "status": status.HTTP_200_OK,
                "username": user.username,
                "book_name": book.book_name,
            }
        )
    else:
        return errors.BookNotAssociated


def get_wishlist(user_id: int, current_session: Session):
    user = current_session.query(app_db.User).get(user_id)
    if not user:
        raise errors.UserNotFound()
    return [
        book
        for book in current_session.query(app_db.models.Book)
        .join(
            app_db.models.user_books_wishlist,
            app_db.models.Book.book_id == app_db.models.user_books_wishlist.c.book_id,
        )
        .filter(app_db.models.user_books_wishlist.c.user_id == user_id)
        .all()
    ]


def update_user_profile(
    user: app_db.User, user_update: schemas.UserUpdate, current_session: Session
):
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    if user_update.first_name:
        user.first_name = user.first_name.title()
    if user_update.second_name:
        user.second_name = user.second_name.title()

    current_session.commit()
    current_session.refresh(user)
    return user
