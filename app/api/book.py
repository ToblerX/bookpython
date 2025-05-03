from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app import db as app_db
from app import services, schemas

book_router = APIRouter()


@book_router.post("/books", tags=["Books"], response_model=schemas.BookModel)
async def create_book(
    book: schemas.BookCreate, current_session: Session = Depends(app_db.get_db)
):
    return services.create_book(book, current_session)


@book_router.get("/books", tags=["Books"], response_model=List[schemas.BookModel])
async def get_books(
    current_session: Session = Depends(app_db.get_db),
    sorting: schemas.SortingBooks = Depends(),
    pagination: schemas.Pagination = Depends(),
):
    return services.get_books(pagination, sorting, current_session)


@book_router.delete("/books", tags=["Books"], response_model=schemas.BookModel)
async def delete_book(
    book: schemas.BookId, current_session: Session = Depends(app_db.get_db)
):
    return services.delete_book(book, current_session)


@book_router.put("/books", tags=["Books"], response_model=schemas.BookModel)
async def update_book(
    book: schemas.BookUpdate, current_session: Session = Depends(app_db.get_db)
):
    return services.update_book(book, current_session)
