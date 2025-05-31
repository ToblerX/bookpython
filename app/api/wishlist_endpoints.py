from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import schemas, services
from .. import db as app_db

wishlist_router = APIRouter()


@wishlist_router.post("/users/me/wishlist", tags=["Wishlist"])
async def add_user_wishlist(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int = Query(..., description="Book id to add to the wishlist."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.add_to_wishlist(current_user.user_id, book_id, current_session)


@wishlist_router.get("/users/me/wishlist", tags=["Wishlist"])
async def get_user_wishlist(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_wishlist(current_user.user_id, current_session)


@wishlist_router.delete("/users/me/wishlist", tags=["Wishlist"])
async def delete_all_from_user_wishlist(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_all_from_wishlist(current_user.user_id, current_session)


@wishlist_router.delete("/users/me/wishlist/{book_id}", tags=["Wishlist"])
async def delete_book_from_user_wishlist(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int,
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_from_wishlist(current_user.user_id, book_id, current_session)
