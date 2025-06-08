from app import db as app_db

GENRES = [
    "Fiction",
    "Non-fiction",
    "Mystery",
    "Fantasy",
    "Science Fiction",
    "Romance",
    "Historical Fiction",
    "Biography",
    "Horror",
    "Young Adult",
    "Children’s Literature",
    "Self-Help",
    "Graphic Novels",
    "Poetry",
    "Classics",
    "Adventure",
    "Literary Fiction",
    "Religion",
    "Science",
    "Travel",
]


def seed_genres():
    current_session = app_db.database.LocalSession()
    genres = GENRES
    for name in genres:
        if (
            not current_session.query(app_db.models.Genre)
            .filter_by(genre_name=name)
            .first()
        ):
            current_session.add(app_db.models.Genre(genre_name=name))
    current_session.commit()
    current_session.close()
