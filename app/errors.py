from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app import config


class BookPythonError(Exception):
    """Base class for exceptions in this api."""

    pass


# === USERS ===
class UserNotFound(BookPythonError):
    """The user was not found."""

    pass


class UserAlreadyExists(BookPythonError):
    """The user already exists."""

    pass


class EmailAlreadyExists(BookPythonError):
    """The email is already registered."""

    pass


class IncorrectUsernameLength(BookPythonError):
    f"""Username must be between {config.USERNAME_MIN} and {config.USERNAME_MAX} characters."""

    pass


class IncorrectPasswordLength(BookPythonError):
    f"""Password must be between {config.PASSWORD_MIN} and {config.PASSWORD_MAX} characters."""

    pass


class IncorrectPasswordFormat(BookPythonError):
    """Password must contain at least one uppercase letter and one special character."""

    pass


class WrongCredentials(BookPythonError):
    """The wrong credentials were provided."""

    pass


class UserNotVerified(BookPythonError):
    """The user is not verified. Check your email."""

    pass


class UserNotActive(BookPythonError):
    """The user is not active."""

    pass


class InvalidToken(BookPythonError):
    """Invalid or expired token."""

    pass


class OnlyAdminsAllowed(BookPythonError):
    """This is allowed only for admins."""

    pass


# === BOOKS ===
class BookNotFound(BookPythonError):
    """The requested book was not found."""

    pass


class BookAlreadyExists(BookPythonError):
    """The book already exists."""

    pass


class IncorrectBookNameLength(BookPythonError):
    f"""The book name must be between {config.BOOK_NAME_MIN} and {config.BOOK_NAME_MAX} characters long."""

    pass


class IncorrectBookDescriptionLength(BookPythonError):
    f"""The book description must be between {config.BOOK_DESC_MIN} and {config.BOOK_DESC_MAX} characters long."""

    pass


class InvalidBookPrice(BookPythonError):
    """Price must be higher than 0."""

    pass


class InvalidBookSupply(BookPythonError):
    """Supply can't be lower than 0."""

    pass


# === GENRES ===
class GenreNotFound(BookPythonError):
    """The genre was not found."""

    pass


class GenreAlreadyExists(BookPythonError):
    """The genre already exists."""

    pass


class IncorrectGenreLength(BookPythonError):
    f"""Genre name must be between {config.GENRE_NAME_MIN} to {config.GENRE_NAME_MAX} characters."""

    pass


class IncorrectGenreName(BookPythonError):
    """Genre name mustn't contain any special characters."""

    pass


class GenreAlreadyAssociated(BookPythonError):
    """The genre was already associated with this book."""

    pass


class GenreNotAssociated(BookPythonError):
    """The genre was not associated with this book."""

    pass


# === IMAGES ===
class ImageNotFound(BookPythonError):
    """The image was not found."""

    pass


class FileMustBeImage(BookPythonError):
    """The provided file is not an image."""

    pass


class CantDeleteDefaultCover(BookPythonError):
    """It is impossible to delete the default cover."""

    pass


## === EXCEPTION HANDLER ===
def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exception: BookPythonError):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler
