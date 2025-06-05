from fastapi import status
from fastapi.responses import JSONResponse
from . import errors, config


def register_exception_handlers(app):
    @app.exception_handler(500)
    async def internal_server_error(request, exception):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong!",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(401)
    async def unauthorized(request, exception):
        return JSONResponse(
            content={
                "message": "You need to be authorized to access this page.",
                "error_code": "not_authorized",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    @app.exception_handler(422)
    async def unprocessable_entity_error(request, exception):
        return JSONResponse(
            content={
                "message": "The entity you entered is not valid.",
                "error_code": "unprocessable_entity",
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "User account already exists.",
                "error_code": "user_exists",
            },
        ),
    )
    app.add_exception_handler(
        errors.EmailAlreadyExists,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Email account already exists.",
                "error_code": "email_exists",
            },
        ),
    )
    app.add_exception_handler(
        errors.IncorrectUsernameLength,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": f"Username must be between {config.USERNAME_MIN} and {config.USERNAME_MAX} characters.",
                "error_code": "incorrect_username_length",
            },
        ),
    )
    app.add_exception_handler(
        errors.IncorrectPasswordLength,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": f"Password must contain from {config.PASSWORD_MIN} to {config.PASSWORD_MAX} characters.",
                "error_code": "incorrect_password_length",
            },
        ),
    )
    app.add_exception_handler(
        errors.IncorrectPasswordFormat,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Password must contain at least one uppercase letter and one special character.",
                "error_code": "incorrect_password_format",
            },
        ),
    )
    app.add_exception_handler(
        errors.WrongCredentials,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
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
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "This book already exists.",
                "error_code": "book_already_exists",
            },
        ),
    )
    app.add_exception_handler(
        errors.IncorrectBookNameLength,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": f"The book name must be between {config.BOOK_NAME_MIN} and {config.BOOK_NAME_MAX} characters long.",
                "error_code": "incorrect_bookname_length",
            },
        ),
    )
    app.add_exception_handler(
        errors.IncorrectBookDescriptionLength,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": f"The book description must be between {config.BOOK_DESC_MIN} and {config.BOOK_DESC_MAX} characters long.",
                "error_code": "incorrect_book_description_length",
            },
        ),
    )
    app.add_exception_handler(
        errors.InvalidBookPrice,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": f"The book price must be higher than 0.",
                "error_code": "invalid_book_price",
            },
        ),
    )
    app.add_exception_handler(
        errors.InvalidBookSupply,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": f"The book supply can't be lower than 0.",
                "error_code": "invalid_book_supply",
            },
        ),
    )
    app.add_exception_handler(
        errors.BookNotAssociated,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "The book is not in the wishlist.",
                "error_code": "book_not_associated",
            },
        ),
    )
    app.add_exception_handler(
        errors.BookAlreadyAssociated,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "The book is already in the wishlist.",
                "error_code": "book_already_associated",
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
        errors.GenreAlreadyExists,
        errors.create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Genre already exists.",
                "error_code": "genre_already_exists",
            },
        ),
    )
    app.add_exception_handler(
        errors.IncorrectGenreName,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Genre name mustn't contain any special characters.",
                "error_code": "incorrect_genre_name",
            },
        ),
    )
    app.add_exception_handler(
        errors.IncorrectGenreLength,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": f"Genre name must be from {config.GENRE_NAME_MIN} to {config.GENRE_NAME_MAX} characters long.",
                "error_code": "incorrect_genre_length",
            },
        ),
    )
    app.add_exception_handler(
        errors.GenreAlreadyAssociated,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
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
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "The provided file is not an image.",
                "error_code": "file_not_image",
            },
        ),
    )
    app.add_exception_handler(
        errors.CantDeleteDefaultCover,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Cannot delete default cover.",
                "error_code": "cannot_delete_default_cover",
            },
        ),
    )
    app.add_exception_handler(
        errors.BookNotFoundInBasket,
        errors.create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "The requested book was not found in the basket.",
                "error_code": "book_not_found_in_basket",
            },
        ),
    )
    app.add_exception_handler(
        errors.QuantityError,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Quantity must be at least 1.",
                "error_code": "quantity_error",
            },
        ),
    )
    app.add_exception_handler(
        errors.BasketEmpty,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Your basket is empty.",
                "error_code": "basket_empty",
            },
        ),
    )
    app.add_exception_handler(
        errors.SupplyTooSmall,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Not enough supply to sell.",
                "error_code": "not_enough_supply",
            },
        ),
    )
    app.add_exception_handler(
        errors.UserDataUndefined,
        errors.create_exception_handler(
            status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Required user data is not defined.",
                "error_code": "user_data_undefined",
            },
        ),
    )
    return {"message": "Exception handlers initialized successfully."}
