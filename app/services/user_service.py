from sqlalchemy.orm import Session
from fastapi import Depends
from .. import schemas, services
from .. import db as app_db


def create_user(user: schemas.UserCreate, current_session: Session):
    new_user = app_db.User(**user.dict())
    current_session.add(new_user)
    current_session.commit()
    current_session.refresh(new_user)
    return new_user


def get_users(current_session: Session):
    return current_session.query(app_db.User).all()
