from fastapi import FastAPI, status
from . import api, errors
import app.db as database
from .init_db import init_db

## === DB INIT ===
database.Base.metadata.create_all(bind=database.engine)
init_db()

## === API INIT ===
app = FastAPI(
    title="Book Python API",
    description="API to handle operations in a book shop.",
    version="1.0",
    openapi_tags=[
        {"name": "Users", "description": "Operations related to user accounts."},
        {"name": "Authentication", "description": "Login and token management."},
        {"name": "Books", "description": "Operations related to books."},
        {"name": "Genres", "description": "Operations related to books' genres."},
    ],
)


## === ERROR HANDLERS ===
app.add_exception_handler(
    errors.UserNotFound,
    errors.create_exception_handler(
        status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "User not found.",
            "error_code": "user_not_found",
        },
    ),
)
app.add_exception_handler(
    errors.UserAlreadyExists,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User account already exists.",
            "error_code": "user_exists",
        },
    ),
)
app.add_exception_handler(
    errors.WrongCredentials,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "You provided wrong credentials.",
            "error_code": "wrong_credentials",
        },
    ),
)
app.add_exception_handler(
    errors.UserNotVerified,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User account not verified.",
            "error_code": "user_not_verified",
        },
    ),
)
app.add_exception_handler(
    errors.UserNotActive,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User account not active.",
            "error_code": "user_not_active",
        },
    ),
)
app.add_exception_handler(
    errors.InvalidToken,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Authentication failed. Wrong token provided.",
            "error_code": "wrong_token",
        },
    ),
)
app.add_exception_handler(
    errors.OnlyAdminsAllowed,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Only administrators can access this page.",
            "error_code": "only_admin_allowed",
        },
    ),
)
app.add_exception_handler(
    errors.BookNotFound,
    errors.create_exception_handler(
        status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Book not found.",
            "error_code": "book_not_found",
        },
    ),
)
app.add_exception_handler(
    errors.BookAlreadyExists,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "This book already exists.",
            "error_code": "book_already_exists",
        },
    ),
)
app.add_exception_handler(
    errors.GenreNotFound,
    errors.create_exception_handler(
        status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Genre not found.",
            "error_code": "genre_not_found",
        },
    ),
)
app.add_exception_handler(
    errors.GenreAlreadyAssociated,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Genre already associated.",
            "error_code": "genre_already_associated",
        },
    ),
)
app.add_exception_handler(
    errors.GenreNotAssociated,
    errors.create_exception_handler(
        status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Genre not associated.",
            "error_code": "genre_not_associated",
        },
    ),
)
app.add_exception_handler(
    errors.ImageNotFound,
    errors.create_exception_handler(
        status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Image not found.",
            "error_code": "image_not_found",
        },
    ),
)
app.add_exception_handler(
    errors.FileMustBeImage,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "The provided file is not an image.",
            "error_code": "file_not_image",
        },
    ),
)
app.add_exception_handler(
    errors.CantDeleteDefaultCover,
    errors.create_exception_handler(
        status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Cannot delete default cover.",
            "error_code": "cannot_delete_default_cover",
        },
    ),
)

## === ROUTERS ===
app.include_router(api.book_router)
app.include_router(api.user_router)
app.include_router(api.genre_router)
