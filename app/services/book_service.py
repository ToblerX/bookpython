import mimetypes
from pathlib import Path

from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from typing import Annotated

from starlette.responses import FileResponse

from app import db as app_db
from app import schemas, config
from app.exceptions import errors
from PIL import Image
import io
import os
import shutil
import re


def create_book(book: schemas.BookCreate, current_session: Session):
    new_book = app_db.models.Book(**book.dict())
    new_book.book_name = new_book.book_name.title()
    new_book.book_cover_path = os.path.join(
        config.IMAGES_BOOKS_PATH, "cover_not_available.jpg"
    )

    check = (
        current_session.query(app_db.models.Book)
        .filter(app_db.models.Book.book_name == new_book.book_name)
        .first()
    )
    if check:
        raise errors.BookAlreadyExists()

    os.mkdir(config.IMAGES_BOOKS_PATH + new_book.book_name)
    current_session.add(new_book)
    current_session.commit()
    current_session.refresh(new_book)
    return new_book


def add_genre_for_book(book_id: int, genre_id: int, current_session: Session):
    genre = current_session.query(app_db.models.Genre).get(genre_id)
    if not genre:
        raise errors.GenreNotFound()

    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    # Check if the book already has the genre
    stmt_check = select(app_db.models.book_genres).where(
        app_db.models.book_genres.c.book_id == book_id,
        app_db.models.book_genres.c.genre_id == genre_id,
    )
    result = current_session.execute(stmt_check).first()
    if result:
        raise errors.GenreAlreadyAssociated()
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


def delete_genre_for_book(book_id: int, genre_id: int, current_session: Session):
    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    genre = current_session.query(app_db.models.Genre).get(genre_id)
    if not genre:
        raise errors.GenreNotFound()
    if genre in book.genres:
        book.genres.remove(genre)
        current_session.commit()
    else:
        raise errors.GenreNotAssociated()


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
        raise errors.BookNotFound()
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
        raise errors.BookNotFound()
    if upd_book.book_name != new_data.book_name:
        os.rename(
            config.IMAGES_BOOKS_PATH + upd_book.book_name,
            config.IMAGES_BOOKS_PATH + new_data.book_name.title(),
        )
    for key, value in new_data.dict(exclude_unset=True).items():
        setattr(upd_book, key, value)
    upd_book.book_name = upd_book.book_name.title()
    current_session.commit()
    current_session.refresh(upd_book)
    return upd_book


def add_image_for_book(contents: bytes, book_id: int, current_session: Session):
    image = Image.open(io.BytesIO(contents))
    book = current_session.query(app_db.models.Book).get(book_id)

    extension = image.format.lower() if image.format else "jpg"

    image_dir = config.IMAGES_BOOKS_PATH + book.book_name

    os.makedirs(image_dir, exist_ok=True)

    existing_files = [
        f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))
    ]
    new_index = len(existing_files)
    filename = f"{new_index}.{extension}"

    image_path = os.path.join(image_dir, filename)
    image.save(image_path)

    return {"status": 200, "path": image_path}


def get_images_for_book(book_id: int, current_session: Session):
    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()

    image_dir = config.IMAGES_BOOKS_PATH + book.book_name

    if not os.path.exists(image_dir):
        return []

    image_files = [
        filename
        for filename in os.listdir(image_dir)
        if os.path.isfile(os.path.join(image_dir, filename))
    ]

    return image_files


def delete_image_by_id(
    book_id: int,
    image_id: int,
    current_session: Session,
):
    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()

    image_dir = os.path.join(config.IMAGES_BOOKS_PATH, book.book_name)

    target_image_path = None
    for filename in os.listdir(image_dir):
        if filename.startswith(f"{image_id}."):
            target_image_path = os.path.join(image_dir, filename)
            os.remove(target_image_path)
            break

    if not target_image_path:
        raise errors.ImageNotFound()

    for filename in os.listdir(image_dir):
        if filename.startswith("cover"):
            continue

        current_id = int(filename.split(".")[0])

        if current_id > image_id:
            new_filename = f"{current_id - 1}.{filename.split('.')[1]}"
            old_image_path = os.path.join(image_dir, filename)
            new_image_path = os.path.join(image_dir, new_filename)
            os.rename(old_image_path, new_image_path)

    return {"status": 200, "path": target_image_path}


def delete_all_images_for_book(
    book_id: int, current_session: Session, delete_cover: bool = False
):
    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    image_dir = os.path.join(config.IMAGES_BOOKS_PATH, book.book_name)
    image_list = []
    for filename in os.listdir(image_dir):
        if re.match(r"^\d", filename):
            file_path = os.path.join(image_dir, filename)
            os.remove(file_path)
            image_list.append(file_path)
    if delete_cover:
        delete_cover_for_book(book_id, current_session)
    return {"status": 200, "deleted": image_list, "cover_deleted": delete_cover}


def get_cover_path_for_book(book_id: int, current_session: Session):
    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    return book.book_cover_path


def get_cover_image_for_book(book_id: int, current_session: Session):
    book = (
        current_session.query(app_db.models.Book)
        .filter(app_db.models.Book.book_id == book_id)
        .first()
    )
    if not book:
        raise errors.BookNotFound()

    image_path = Path(book.book_cover_path)
    if not image_path.is_file():
        raise errors.ImageNotFound  # optional custom error

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type:
        mime_type = "application/octet-stream"  # fallback

    return FileResponse(
        path=str(image_path),
        media_type=mime_type,
        filename=image_path.name,
    )


def update_cover_for_book(contents: bytes, book_id: int, current_session: Session):
    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    image = Image.open(io.BytesIO(contents))
    extension = image.format.lower() if image.format else "jpg"
    image_dir = config.IMAGES_BOOKS_PATH + book.book_name
    filename = f"cover.{extension}"
    image_path = image_dir + "/" + filename
    image.save(image_path)

    if book.book_cover_path == config.DEFAULT_COVER_PATH:
        book.book_cover_path = image_path

    current_session.commit()
    current_session.refresh(book)

    return {"status": 200, "new_cover": image_path}


def delete_cover_for_book(
    book_id: int,
    current_session: Session,
):
    book = current_session.query(app_db.models.Book).get(book_id)
    if book.book_cover_path == config.DEFAULT_COVER_PATH:
        raise errors.CantDeleteDefaultCover()

    image_dir = config.IMAGES_BOOKS_PATH + book.book_name

    for filename in os.listdir(image_dir):
        if filename.startswith("cover"):
            os.remove(os.path.join(image_dir, filename))
            break

    old_cover = book.book_cover_path
    book.book_cover_path = config.DEFAULT_COVER_PATH

    current_session.commit()
    current_session.refresh(book)

    return {
        "status": 200,
        "prev_cover": old_cover,
        "new_cover": config.DEFAULT_COVER_PATH,
    }


def edit_supply_by_id(
    book_id: int,
    amount: int,
    current_session: Session,
):
    book = current_session.query(app_db.models.Book).get(book_id)
    if not book:
        raise errors.BookNotFound()
    if amount < 0 and abs(amount) > book.supply:
        raise errors.InvalidBookSupply()
    book.supply += amount
    current_session.commit()
    current_session.refresh(book)
    return book
