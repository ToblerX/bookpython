from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, services
from .. import db as app_db


user_router = APIRouter()


@user_router.post("/users", tags=["Users"], response_model=schemas.UserModel)
async def create_user(
    user: schemas.UserCreate, current_session: Session = Depends(app_db.get_db)
):
    return services.create_user(user, current_session)


@user_router.get("/users", tags=["Users"], response_model=List[schemas.UserCreate])
async def get_users(current_session: Session = Depends(app_db.get_db)):
    return services.get_users(current_session)
