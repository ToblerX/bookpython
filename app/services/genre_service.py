from sqlalchemy.orm import Session
from .. import schemas
from .. import db as app_db


def create_genre(genre: schemas.GenreCreate, current_session: Session):
    new_genre = app_db.models.Genre(**genre.dict())
    new_genre.genre_name = genre.genre_name.title()
    current_session.add(new_genre)
    current_session.commit()
    current_session.refresh(new_genre)
    return new_genre


def get_genres(current_session: Session):
    return current_session.query(app_db.models.Genre).all()


def delete_genre_by_id(genre_id: int, current_session: Session):
    del_genre = (
        current_session.query(app_db.models.Genre)
        .filter(app_db.models.Genre.genre_id == genre_id)
        .first()
    )
    current_session.delete(del_genre)
    current_session.commit()
    return del_genre
