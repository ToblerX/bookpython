from sqlalchemy.orm import Session
from app import db as app_db
from app import schemas


def create_book(book: schemas.BookCreate, current_session: Session):
    new_book = app_db.models.Book(**book.dict())
    current_session.add(new_book)
    current_session.commit()
    current_session.refresh(new_book)
    return new_book


def get_books(current_session: Session):
    return current_session.query(app_db.models.Book).all()
