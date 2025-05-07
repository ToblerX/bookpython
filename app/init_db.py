from sqlalchemy import select, func
import app.db as database
from .config import GENRES


def init_db():
    with database.LocalSession() as session:
        count = session.execute(
            select(func.count()).select_from(database.models.Genre)
        ).scalar()
        if count == 0:
            print("🌱 Seeding genres...")
            seed_genres()
            print("✅  Genres seeded.")


# TRUNCATE TABLE genres RESTART IDENTITY CASCADE;
def seed_genres():
    session = database.LocalSession()
    genres = GENRES
    for name in genres:
        if not session.query(database.models.Genre).filter_by(genre_name=name).first():
            session.add(database.models.Genre(genre_name=name))
    session.commit()
    session.close()


if __name__ == "__main__":
    init_db()
    print("✅ DB initialized.")
