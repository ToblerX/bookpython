from fastapi import FastAPI
from . import api, handlers, middleware
import app.db as database
from .init_db import init_db

## === DB INIT ===
database.Base.metadata.create_all(bind=database.engine)
init_db()

## === API INIT ===
app = FastAPI(
    title="Book Python API",
    description="API to handle operations in a book shop.",
    version="1.0",
    openapi_tags=[
        {"name": "Non-Admin", "description": "Operations for all users."},
        {"name": "Authentication", "description": "Login and token management."},
        {"name": "Users", "description": "Operations related to user accounts."},
        {"name": "Basket", "description": "Operations related to baskets."},
        {"name": "Orders", "description": "Operations related to orders."},
        {"name": "Wishlist", "description": "Operations related to wishlist."},
        {"name": "Books", "description": "Operations related to books."},
        {"name": "Admin Only", "description": "Operations only for admins or system."},
        {
            "name": "Users Admin",
            "description": "Operations related to user accounts that can only be performed by admins.",
        },
        {
            "name": "Basket Admin",
            "description": "Operations related to baskets that can only be performed by admins.",
        },
        {
            "name": "Orders Admin",
            "description": "Operations related to orders that can only be performed by admins.",
        },
        {
            "name": "Wishlist Admin",
            "description": "Operations related to wishlist that can only be performed by admins.",
        },
        {
            "name": "Books Admin",
            "description": "Operations related to books that can only be performed by admins.",
        },
        {
            "name": "Genres Admin",
            "description": "Operations related to books' genres that can only be performed by admins.",
        },
    ],
)

handlers.register_exception_handlers(app)

middleware.register_middleware(app)

## === ROUTERS ===
app.include_router(api.book_router)
app.include_router(api.user_router)
app.include_router(api.genre_router)

app.include_router(api.basket_router)
