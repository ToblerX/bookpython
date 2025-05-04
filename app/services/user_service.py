from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import schemas
from .. import db as app_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(user: schemas.UserCreate, current_session: Session):
    new_user = app_db.User(**user.dict())
    new_user.hashed_password = get_password_hash(user.hashed_password)
    current_session.add(new_user)
    current_session.commit()
    current_session.refresh(new_user)
    return new_user


def get_users(current_session: Session):
    return current_session.query(app_db.User).all()
