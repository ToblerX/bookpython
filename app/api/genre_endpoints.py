from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app import db as app_db
from app import services, schemas

genre_router = APIRouter()


@genre_router.post("/genres", tags=["Genres"], response_model=schemas.GenreModel)
async def create_genre(
    genre: schemas.GenreCreate, db: Session = Depends(app_db.get_db)
):
    return services.create_genre(genre, db)


@genre_router.get("/genres", tags=["Genres"], response_model=List[schemas.GenreModel])
async def get_genres(db: Session = Depends(app_db.get_db)):
    return services.get_genres(db)
