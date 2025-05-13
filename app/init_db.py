from sqlalchemy import select, func
from . import db as app_db
from . import config, services


def init_db():
    with app_db.database.LocalSession() as session:
        count = session.execute(
            select(func.count()).select_from(app_db.models.Genre)
        ).scalar()
        if count == 0:
            seed_genres()
            print("✅  Genres seeded.")
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
