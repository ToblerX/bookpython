from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends, Query, Path
from sqlalchemy.orm import Session
from app import db as app_db
from app import services, schemas, errors

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


@book_router.delete(
    "/books/{book_id}", tags=["Books"], response_model=schemas.BookModel
)
async def delete_book(
    book_id: int = Path(..., description="Id of the book to delete."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_book_by_id(book_id, current_session)


@book_router.put("/books/{book_id}", tags=["Books"], response_model=schemas.BookModel)
async def update_book(
    new_data: schemas.BookUpdate,
    book_id: int = Path(..., description="Id of the book to update."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.update_book_by_id(new_data, book_id, current_session)


@book_router.get("/books/{book_id}", tags=["Books"], response_model=schemas.BookModel)
async def get_book_by_id(
    book_id: int = Path(..., description="ID of the book to get."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_book_by_id(book_id, current_session)


@book_router.post("/books/{book_id}/genres", tags=["Books"])
async def add_genre_for_book(
    book_id: int = Path(..., description="ID of the book"),
    genre_id: int = Query(..., description="ID of the genre to add"),
    current_session: Session = Depends(app_db.get_db),
):
    return services.add_genre_for_book(book_id, genre_id, current_session)


@book_router.get("/books/{book_id}/genres", tags=["Books"], response_model=List[str])
async def get_genre_for_book(
    book_id: int = Path(..., description="ID of the book"),
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_genres_for_book(book_id, current_session)


@book_router.delete("/books/{book_id}/genres", tags=["Books"])
async def delete_genre_for_book(
    book_id: int = Path(..., description="ID of the book"),
    genre_id: int = Query(..., description="ID of the genre to delete"),
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_genre_for_book(book_id, genre_id, current_session)


@book_router.post("/books/{book_id}/images", tags=["Books"])
async def add_image_for_book(
    file: UploadFile = File(...),
    book_id: int = Path(..., description="ID of the book"),
    current_session: Session = Depends(app_db.get_db),
):
    if not file.content_type.startswith("image/"):
        raise errors.FileMustBeImage()
    contents = await file.read()
    return services.add_image_for_book(contents, book_id, current_session)


@book_router.get("/books/{book_id}/images", tags=["Books"])
async def get_images_for_book(
    book_id: int = Path(..., description="ID of the book"),
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_images_for_book(book_id, current_session)


@book_router.delete("/books/{book_id}/images", tags=["Books"])
async def delete_image_for_book(
    book_id: int = Path(..., description="ID of the book"),
    image_id: int = Query(..., description="ID of the image to delete."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_image_by_id(book_id, image_id, current_session)


@book_router.delete("/books/{book_id}/delete_all_images", tags=["Books"])
async def delete_images_for_book(
    book_id: int = Path(..., description="ID of the book"),
    current_session: Session = Depends(app_db.get_db),
    delete_cover: bool = False,
):
    return services.delete_all_images_for_book(book_id, current_session, delete_cover)


@book_router.get("/books/{book_id}/cover", tags=["Books"])
async def get_cover_for_book(
    book_id: int = Path(..., description="ID of the book"),
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_cover_path_for_book(book_id, current_session)


@book_router.put("/books/{book_id}/cover", tags=["Books"])
async def update_cover_for_book(
    file: UploadFile = File(...),
    book_id: int = Path(..., description="ID of the book"),
    current_session: Session = Depends(app_db.get_db),
):
    if not file.content_type.startswith("image/"):
        raise errors.FileMustBeImage()
    contents = await file.read()
    return services.update_cover_for_book(contents, book_id, current_session)


@book_router.delete("/books/{book_id}/cover", tags=["Books"])
async def delete_cover_for_book(
    book_id: int = Path(..., description="ID of the book"),
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_cover_for_book(book_id, current_session)
