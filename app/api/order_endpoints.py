from typing import Annotated, Literal

from fastapi import Depends, Query, APIRouter
from fastapi.background import BackgroundTasks
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import schemas, services
from app.exceptions import errors
from app import db as app_db


order_router = APIRouter()


@order_router.post("/users/me/orders", tags=["Orders"])
async def create_order(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    bg_tasks: BackgroundTasks,
    delivery_method: Literal["courier", "pickup", "parcel_locker"] = Query(
        ..., description="Delivery method: 'courier', 'pickup', or 'parcel_locker'"
    ),
    current_session: Session = Depends(app_db.get_db),
):
    user_full = (
        current_session.query(app_db.models.User)
        .filter(app_db.models.User.user_id == current_user.user_id)
        .first()
    )
    # Check required delivery fields + email
    required_fields = [
        user_full.email,
        user_full.first_name,
        user_full.second_name,
        user_full.street_address,
        user_full.city,
        user_full.state,
        user_full.postal_code,
        user_full.country,
        user_full.phone_number,
    ]
    if any(field is None or field == "" for field in required_fields):
        raise errors.UserDataUndefined

    basket_items = services.get_basket(current_user.user_id, current_session)

    if not basket_items:
        raise errors.BasketEmpty

    total_price = sum(item.book.book_price * item.quantity for item in basket_items)

    order_items = [
        schemas.OrderItemCreate(book_id=item.book.book_id, quantity=item.quantity)
        for item in basket_items
    ]

    order_data = schemas.OrderCreate(
        user_id=current_user.user_id,
        items=order_items,
        delivery_method=delivery_method,
        total_cost=total_price,
    )

    order = services.create_order(order_data, current_session)
    services.clear_basket(current_user.user_id, current_session)

    order_items = current_session.query(app_db.models.OrderItem).filter(
        app_db.models.OrderItem.order_id == order.order_id
    )

    bg_tasks.add_task(
        services.send_order_information_email,
        user_full.email,
        order.order_id,
        total_price,
        order_items,
    )

    return JSONResponse(
        status_code=201,
        content={
            "message": "Order created successfully",
            "order_id": order.order_id,
            "total_cost": order.total_cost,
            "status": order.status,
            "created_at": order.created_at.isoformat(),
        },
    )


@order_router.get("/users/me/orders", tags=["Orders"])
async def get_user_orders(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    orders = services.get_user_orders(current_user.user_id, current_session)
    return orders


@order_router.get("/admin/users/{user_id}/orders", tags=["Orders Admin"])
async def get_user_orders_by_id(
    user_id: int,
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
    current_session: Session = Depends(app_db.get_db),
):
    if current_user.role != "admin":
        raise errors.OnlyAdminsAllowed
    orders = services.get_user_orders(user_id, current_session)
    return orders


@order_router.patch("/admin/orders/{order_id}", tags=["Orders Admin"])
async def update_order_status(
    order_id: int,
    order_status: Literal["pending", "completed", "cancelled"] = Query(
        ..., description="Delivery method: 'pending', 'completed', or 'cancelled'"
    ),
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
    current_session: Session = Depends(app_db.get_db),
):
    if current_user.role != "admin":
        raise errors.OnlyAdminsAllowed
    return services.set_order_status(order_id, order_status, current_session)
