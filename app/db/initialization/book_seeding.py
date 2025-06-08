import os
import requests

from app import db as app_db, schemas
from app import config

BOOKS = [
    (
        schemas.BookInit(
            book_id=0,
            book_name="Crooked House",
            book_author="Agatha Christie",
            book_description="Crooked House is a work of detective fiction by Agatha Christie first published in the US by Dodd, Mead and Company in March 1949 and in the UK by the Collins Crime Club on 23 May of the same year. The action takes place in and near London in the autumn of 1947. Christie said the titles of this novel and Ordeal by Innocence were her favourites amongst her own works.",
            book_price=15,
            supply=100,
            book_cover_path=os.path.join(
                config.IMAGES_BOOKS_PATH, "Crooked House", "cover.jpg"
            ),
        ),
        [1, 3, 6],
        "https://m.media-amazon.com/images/I/714wbWkDOUL._AC_UF1000,1000_QL80_.jpg",
    )
]


def seed_books():
    current_session = app_db.database.LocalSession()
    books = BOOKS
    for book in books:
        if (
            not current_session.query(app_db.models.Book)
            .filter_by(book_name=book[0].book_name)
            .first()
        ):
            book_img_dir = os.path.join(config.IMAGES_BOOKS_PATH, book[0].book_name)
            os.mkdir(book_img_dir)
            new_book = app_db.models.Book(**book[0].dict())
            current_session.add(new_book)
            response = requests.get(book[2])
            with open(f"{book_img_dir}/cover.jpg", "wb") as f:
                f.write(response.content)
            current_session.commit()
            for genre_id in book[1]:
                stmt = app_db.models.book_genres.insert().values(
                    book_id=book[0].book_id, genre_id=genre_id
                )
                current_session.execute(stmt)
                current_session.commit()
    current_session.commit()
    current_session.close()
