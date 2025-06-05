from sqlalchemy import select
from sqlalchemy.orm import Session

from starlette import status
from starlette.responses import JSONResponse

from ..exceptions import errors
from .. import db as app_db


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


def delete_all_from_wishlist(user_id: int, current_session: Session):
    user = current_session.get(app_db.User, user_id)
    if not user:
        raise errors.UserNotFound()

    user.wishlist.clear()
    current_session.commit()

    return JSONResponse({"message": "All books removed from wishlist."})
