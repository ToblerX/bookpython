from datetime import timedelta
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi.background import BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from .. import schemas, services, config, errors
from .. import db as app_db

user_router = APIRouter()


@user_router.post("/signup", tags=["Users"])
async def create_user(
    user: schemas.UserCreate,
    bg_tasks: BackgroundTasks,
    current_session: Session = Depends(app_db.get_db),
):
    user_exists = services.user_exists(user, current_session)
    if user_exists:
        raise errors.UserAlreadyExists()

    email_exists = services.email_exists(user, current_session)
    if email_exists:
        raise errors.EmailAlreadyExists()

    new_user = services.create_user(user, current_session)

    bg_tasks.add_task(services.send_verification_email, user.email)

    return {
        "message": "Account created, check your email to verify your account",
        "user": new_user,
    }


@user_router.get("/verify/{token}", tags=["Users"])
async def verify_user_account(
    token: str,
    current_session: Session = Depends(app_db.get_db),
):
    token_data = services.decode_url_safe_token(token)
    user_email = token_data.get("email")
    if user_email:
        user = services.get_user_by_email(user_email, current_session)
        if not user:
            raise errors.UserNotFound()
        services.update_user(user, {"verified": True}, current_session)
        return JSONResponse(
            {"message": "Account verified successfully"}, status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={"message": "Error occurred during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@user_router.get("/users", tags=["Users"], response_model=List[schemas.UserModel])
async def get_users(
    current_user: schemas.UserOut = Depends(services.get_current_active_user),
    current_session: Session = Depends(app_db.get_db),
):
    if current_user.role != "admin":
        raise errors.OnlyAdminsAllowed()
    return services.get_users(current_session)


@user_router.get("/users/me/", tags=["Users"], response_model=schemas.UserModel)
async def get_user(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
):
    return current_user


@user_router.patch("/users/me", tags=["Users"], response_model=schemas.UserModel)
async def update_user_profile(
    user_update: schemas.UserUpdate,
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    session: Session = Depends(app_db.get_db),
):
    user_in_db = services.get_user(current_user.username, session)
    if not user_in_db:
        raise errors.UserNotFound()
    return services.update_user_profile(user_in_db, user_update, session)


@user_router.post("/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    current_session: Session = Depends(app_db.database.get_db),
):
    user = services.authenticate_user(
        form_data.username, form_data.password, current_session
    )
    if not user:
        raise errors.WrongCredentials()
    if not user.verified:
        await services.send_verification_email(user.email)
        raise errors.UserNotVerified()
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@user_router.post("/password-reset-request", tags=["Users"])
async def password_reset_request(email_data: schemas.PasswordResetRequestModel):
    await services.send_password_reset_email(email_data.email)
    return JSONResponse(
        content={"message": "Please check your email to reset your password"},
        status_code=status.HTTP_200_OK,
    )


@user_router.post("/password-reset-confirm/{token}", tags=["Users"])
async def reset_account_password(
    token: str,
    password: schemas.PasswordResetConfirmModel,
    current_session: Session = Depends(app_db.get_db),
):
    if password.new_password != password.confirm_new_password:
        raise HTTPException(
            detail="New password and confirm new password do not match",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    token_data = services.decode_url_safe_token(token)
    user_email = token_data.get("email")
    if user_email:
        user = services.get_user_by_email(user_email, current_session)
        if not user:
            raise errors.UserNotFound()
        services.update_user(
            user,
            {"hashed_password": services.get_password_hash(password.new_password)},
            current_session,
        )
        return JSONResponse(
            {"message": "Password reset successfully"}, status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={"message": "Error occurred during password reset"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@user_router.post("/users/me/wishlist", tags=["Users"])
async def add_user_wishlist(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int = Query(..., description="Book id to add to the wishlist."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.add_to_wishlist(current_user.user_id, book_id, current_session)


@user_router.get("/users/me/wishlist", tags=["Users"])
async def get_user_wishlist(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_wishlist(current_user.user_id, current_session)


@user_router.delete("/users/me/wishlist", tags=["Users"])
async def delete_from_user_wishlist(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int = Query(..., description="Book id to delete from the wishlist."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_from_wishlist(current_user.user_id, book_id, current_session)


@user_router.post("/users/me/basket", tags=["Users"])
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


@user_router.get("/users/me/basket", tags=["Users"])
async def get_user_basket(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    return services.get_basket(current_user.user_id, current_session)


@user_router.delete("/users/me/basket", tags=["Users"])
async def delete_from_basket(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    book_id: int = Query(..., description="Book id to remove from basket."),
    current_session: Session = Depends(app_db.get_db),
):
    return services.delete_from_basket(current_user.user_id, book_id, current_session)


@user_router.put("/users/me/basket", tags=["Users"])
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


@user_router.post("/users/me/orders", tags=["Orders"])
async def create_order(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    delivery_method: str = Query(..., description="Delivery method chosen by the user"),
    current_session: Session = Depends(app_db.get_db),
):
    # Step 1: Get user's basket
    basket_items = services.get_basket(current_user.user_id, current_session)

    if not basket_items:
        raise HTTPException(status_code=400, detail="Your basket is empty.")

    # Step 2: Calculate total price
    total_price = sum(item.book.book_price * item.quantity for item in basket_items)

    # Step 3: Convert basket items to order items
    order_items = [
        schemas.OrderItemCreate(book_id=item.book.book_id, quantity=item.quantity)
        for item in basket_items
    ]

    # Step 4: Prepare order data including delivery_method and total_price
    order_data = schemas.OrderCreate(
        user_id=current_user.user_id,
        items=order_items,
        delivery_method=delivery_method,
        total_cost=total_price,
    )

    # Step 5: Create the order
    order = services.create_order(order_data, current_session)

    # Step 6: Clear the user's basket if order was successful
    services.clear_basket(current_user.user_id, current_session)

    return order


@user_router.get("/users/me/orders", tags=["Orders"])
async def get_user_orders(
    current_user: Annotated[
        schemas.UserDecode, Depends(services.get_current_active_user)
    ],
    current_session: Session = Depends(app_db.get_db),
):
    orders = services.get_user_orders(current_user.user_id, current_session)
    return orders
