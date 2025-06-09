from sqlalchemy import select, func
from app import db as app_db
from app import config, services
from .book_seeding import seed_books
from .genre_seeding import seed_genres


def init_db(
    create_admin: bool = True, init_genres: bool = True, init_books: bool = True
):
    with app_db.database.LocalSession() as session:
        count = session.execute(
            select(func.count()).select_from(app_db.models.Genre)
        ).scalar()
        if count == 0 and init_genres:
            seed_genres()
            print("✅  Genres seeded.")
        count = session.execute(
            select(func.count()).select_from(app_db.models.Book)
        ).scalar()
        if count == 0 and init_books:
            seed_books()
            print("✅  Books seeded.")
        if create_admin:
            create_admin_user()


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

# TRUNCATE TABLE users, genres, books, user_books, book_genres, baskets, orders, order_items RESTART IDENTITY CASCADE;
# DROP TABLE users, genres, user_books, book_genres, books, baskets, orders, order_items
