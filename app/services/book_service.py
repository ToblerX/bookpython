from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException
from typing import Annotated
from app import db as app_db
from app import schemas, config
import os
import shutil


def create_book(book: schemas.BookCreate, current_session: Session):
    new_book = app_db.models.Book(**book.dict())
    new_book.book_name = new_book.book_name.title()

    check = (
        current_session.query(app_db.models.Book)
        .filter(app_db.models.Book.book_name == new_book.book_name)
        .first()
    )
    if check:
        raise HTTPException(status_code=400, detail="Book already exists")

    os.mkdir(config.IMAGES_BOOKS_PATH + new_book.book_name)
    current_session.add(new_book)
    current_session.commit()
    current_session.refresh(new_book)
    return new_book


def add_genre_for_book(book_id: int, genre_id: int, current_session: Session):
    genre = current_session.query(app_db.models.Genre).get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Check if the book already has the genre
    stmt_check = select(app_db.models.book_genres).where(
        app_db.models.book_genres.c.book_id == book_id,
        app_db.models.book_genres.c.genre_id == genre_id,
    )
    result = current_session.execute(stmt_check).first()
    if result:
        raise HTTPException(
            status_code=400, detail="Genre already associated with this book"
        )
    stmt = app_db.models.book_genres.insert().values(book_id=book_id, genre_id=genre_id)
    current_session.execute(stmt)
    current_session.commit()
    return {"book": book.book_name, "genre": genre.genre_name}


def get_genres_for_book(book_id: int, current_session: Session):
    return [
        genre.genre_name
        for genre in current_session.query(app_db.models.Genre)
        .join(
            app_db.models.book_genres,
            app_db.models.Genre.genre_id == app_db.models.book_genres.c.genre_id,
        )
        .filter(app_db.models.book_genres.c.book_id == book_id)
        .all()
    ]


def get_books(
    pagination: schemas.Pagination,
    sorting: Annotated[schemas.SortingBooks, Depends()],
    current_session: Session,
):
    sort_column = getattr(app_db.models.Book, sorting.sort_by)
    sort_order = asc(sort_column) if sorting.order == "asc" else desc(sort_column)

    query = current_session.query(app_db.models.Book)

    # Join with genres and filter by genre names, if provided
    if sorting.genres:
        genre_names = [genre.genre_name for genre in sorting.genres]
        query = query.join(app_db.models.Book.genres).filter(
            app_db.models.Genre.genre_name.in_(genre_names)
        )

    query = (
        query.options(joinedload(app_db.models.Book.genres))
        .order_by(sort_order)
        .offset(pagination.skip)
        .limit(pagination.limit)
    )

    return query.all()


def get_book_by_id(book_id: int, current_session: Session):
    return current_session.query(app_db.models.Book).get(book_id)


def delete_book_by_id(
    book_id: int,
    current_session: Session,
):
    del_book = (
        current_session.query(app_db.models.Book)
        .filter(app_db.models.Book.book_id == book_id)
        .first()
    )
    if not del_book:
        raise HTTPException(status_code=404, detail="Book not found")
    shutil.rmtree(config.IMAGES_BOOKS_PATH + del_book.book_name)
    current_session.delete(del_book)
    current_session.commit()
    return del_book


def update_book_by_id(
    new_data: schemas.BookUpdate, book_id: int, current_session: Session
):
    upd_book = (
        current_session.query(app_db.models.Book)
        .filter(app_db.models.Book.book_id == book_id)
        .first()
    )
    if not upd_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in new_data.dict(exclude_unset=True).items():
        setattr(upd_book, key, value)
    current_session.commit()
    current_session.refresh(upd_book)
    return upd_book
