import os
import requests

from sqlalchemy import select, func
from . import db as app_db, schemas
from . import config, services

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


def init_db():
    with app_db.database.LocalSession() as session:
        count = session.execute(
            select(func.count()).select_from(app_db.models.Genre)
        ).scalar()
        if count == 0:
            seed_genres()
            print("✅  Genres seeded.")
        count = session.execute(
            select(func.count()).select_from(app_db.models.Book)
        ).scalar()
        if count == 0:
            seed_books()
            print("✅  Books seeded.")
        create_admin_user()


# TRUNCATE TABLE genres RESTART IDENTITY CASCADE;
def seed_genres():
    current_session = app_db.database.LocalSession()
    genres = config.GENRES
    for name in genres:
        if (
            not current_session.query(app_db.models.Genre)
            .filter_by(genre_name=name)
            .first()
        ):
            current_session.add(app_db.models.Genre(genre_name=name))
    current_session.commit()
    current_session.close()


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


def create_admin_user():
    current_session = app_db.LocalSession()
    try:
        if (
            current_session.query(app_db.models.User)
            .filter(app_db.models.User.role == "admin")
            .first()
        ):
            print("Admin user already exists.")
            return
        admin = app_db.models.User(
            user_id=0,
            role="admin",
            username="admin",
            email="admin@gmail.com",
            verified=True,
            hashed_password=services.get_password_hash(config.ADMIN_PASSWORD),
            disabled=False,
            first_name="Admin",
            second_name="User",
            street_address="123 Admin St",
            city="Adminville",
            state="Admin State",
            postal_code="00000",
            country="Adminland",
            phone_number="+10000000000",
        )
        current_session.add(admin)
        current_session.commit()
        current_session.refresh(admin)
        print("✅  Admin user created.")
        return admin
    finally:
        current_session.close()


if __name__ == "__main__":
    init_db()
    print("✅ DB initialized.")
