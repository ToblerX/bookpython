from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import Annotated
from app import db as app_db
from app import schemas


def create_book(book: schemas.BookCreate, current_session: Session):
    new_book = app_db.models.Book(**book.dict())
    current_session.add(new_book)
    current_session.commit()
    current_session.refresh(new_book)
    return new_book


def add_genre_for_book(book_id: int, genre_id: int, current_session: Session):
    stmt = app_db.models.book_genres.insert().values(book_id=book_id, genre_id=genre_id)
    current_session.execute(stmt)
    current_session.commit()
    return {"book_id": book_id, "genre_id": genre_id}


def get_genres_for_book(book_id: int, current_session: Session):
    return [
        genre_id
        for (genre_id,) in current_session.query(
            app_db.models.book_genres.c.genre_id
        )  # Accessing column using .c
        .filter_by(book_id=book_id)
        .all()
    ]


def get_books(
    pagination: schemas.Pagination,
    sorting: Annotated[schemas.SortingBooks, Depends()],
    current_session: Session,
):
    sort_column = func.lower(getattr(app_db.models.Book, sorting.sort_by))
    sort_order = asc(sort_column) if sorting.order == "asc" else desc(sort_column)
    return (
        current_session.query(app_db.models.Book)
        .order_by(sort_order)
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )


def delete_book(
    book: schemas.BookId,
    current_session: Session,
):
    del_book = (
        current_session.query(app_db.models.Book)
        .filter(app_db.models.Book.book_id == book.book_id)
        .first()
    )
    if not del_book:
        raise HTTPException(status_code=404, detail="Book not found")
    current_session.delete(del_book)
    current_session.commit()
    return del_book


def update_book(book: schemas.BookUpdate, current_session: Session):
    upd_book = (
        current_session.query(app_db.models.Book)
        .filter(app_db.models.Book.book_id == book.book_id)
        .first()
    )
    if not upd_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(upd_book, key, value)
    current_session.commit()
    current_session.refresh(upd_book)
    return upd_book
