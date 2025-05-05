from sqlalchemy.orm import Session
from .. import schemas
from .. import db as app_db


def create_genre(genre: schemas.GenreCreate, db: Session):
    new_genre = app_db.models.Genre(**genre.dict())
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre


def get_genres(db: Session):
    return db.query(app_db.models.Genre).all()
