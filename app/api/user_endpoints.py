from datetime import timedelta
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, services, config
from .. import db as app_db


user_router = APIRouter()


@user_router.post("/users", tags=["Users"], response_model=schemas.UserModel)
async def create_user(
    user: schemas.UserCreate,
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
    current_session: Session = Depends(app_db.get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create new users.",
        )
    return services.create_user(user, current_session)


@user_router.get("/users", tags=["Users"], response_model=List[schemas.UserModel])
async def get_users(
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
    current_session: Session = Depends(app_db.get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can view user list.",
        )
    return services.get_users(current_session)


@user_router.get("/users/me/", tags=["Users"], response_model=schemas.UserModel)
async def get_user(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
):
    return current_user


@user_router.post("/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    current_session: Session = Depends(app_db.database.get_db),
):
    user = services.authenticate_user(
        form_data.username, form_data.password, current_session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
