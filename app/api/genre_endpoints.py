from typing import List
from fastapi import APIRouter
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from app import db as app_db, errors
from app import services, schemas

genre_router = APIRouter()


@genre_router.post("/genres", tags=["Genres Admin"], response_model=schemas.GenreModel)
async def create_genre(
    genre: schemas.GenreCreate,
    db: Session = Depends(app_db.get_db),
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
):
    if current_user.role != "admin":
        raise errors.OnlyAdminsAllowed()
    check = (
        db.query(app_db.models.Genre)
        .filter(app_db.models.Genre.genre_name == genre.genre_name)
        .first()
    )
    if check:
        raise errors.GenreAlreadyExists()
    return services.create_genre(genre, db)


@genre_router.get(
    "/genres", tags=["Genres Admin"], response_model=List[schemas.GenreModel]
)
async def get_genres(
    db: Session = Depends(app_db.get_db),
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
):
    if current_user.role != "admin":
        raise errors.OnlyAdminsAllowed()
    return services.get_genres(db)


@genre_router.put("/genres/{genre_id}", tags=["Genres Admin"])
async def update_genre(
    genre_data: schemas.GenreUpdate,
    genre_id: int = Path(..., description="ID of genre to update."),
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
    db: Session = Depends(app_db.get_db),
):
    if current_user.role != "admin":
        raise errors.OnlyAdminsAllowed()
    return services.update_genre_by_id(genre_id, genre_data, db)


@genre_router.delete(
    "/genres/{genre_id}", tags=["Genres Admin"], response_model=schemas.GenreModel
)
async def delete_genre_by_id(
    genre_id: int = Path(..., description="ID of genre to delete."),
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
    db: Session = Depends(app_db.get_db),
):
    if current_user.role != "admin":
        raise errors.OnlyAdminsAllowed()
    check = (
        db.query(app_db.models.Genre)
        .filter(app_db.models.Genre.genre_id == genre_id)
        .first()
    )
    if not check:
        raise errors.GenreNotFound()
    return services.delete_genre_by_id(genre_id, db)
