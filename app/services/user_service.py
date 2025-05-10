from datetime import timedelta, datetime
from fastapi import HTTPException, Depends
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from .. import schemas, config
from .. import db as app_db
import jwt


def get_password_hash(password):
    return config.PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    return config.PWD_CONTEXT.verify(plain_password, hashed_password)


def create_user(user: schemas.UserCreate, current_session: Session):
    new_user = app_db.User(**user.dict())
    new_user.hashed_password = get_password_hash(user.hashed_password)
    current_session.add(new_user)
    current_session.commit()
    current_session.refresh(new_user)
    return new_user


def get_users(current_session: Session):
    return current_session.query(app_db.User).all()


def get_user(username: str, current_session: Session):
    user_dict = (
        current_session.query(app_db.User)
        .filter(app_db.User.username == username)
        .first()
    )
    if user_dict:
        return user_dict
    raise HTTPException(status_code=404, detail="User not found")


def authenticate_user(username: str, password: str, current_session: Session):
    user = get_user(username, current_session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(config.oauth2_scheme)],
    current_session: Session = Depends(app_db.database.get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, current_session)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[schemas.UserModel, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
