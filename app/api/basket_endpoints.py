from typing import Annotated

from fastapi import Depends, Query, Body, APIRouter
from sqlalchemy.orm import Session

from app import schemas, services
from app import db as app_db


basket_router = APIRouter()


@basket_router.post("/users/me/basket", tags=["Basket"])
async def add_to_basket(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int = Query(..., description="Book id to add to the basket."),
    quantity: int = Query(1, description="Quantity to add to the basket."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.add_to_basket(
        current_user.user_id, book_id, quantity, current_session
    )


@basket_router.get("/users/me/basket", tags=["Basket"])
async def get_user_basket(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_basket(current_user.user_id, current_session)


@basket_router.put("/users/me/basket", tags=["Basket"])
async def update_basket_quantity(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int = Query(..., description="Book id to update quantity."),
    update_data: schemas.BasketUpdate = Body(..., description="Updated quantity."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.update_basket_quantity(
        current_user.user_id, book_id, update_data, current_session
    )


@basket_router.delete("/users/me/basket", tags=["Basket"])
async def delete_all_from_basket(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    return services.clear_basket(current_user.user_id, current_session)


@basket_router.delete("/users/me/basket/{book_id}", tags=["Basket"])
async def delete_item_from_basket(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int,
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_from_basket(current_user.user_id, book_id, current_session)
