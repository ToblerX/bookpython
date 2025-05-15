from fastapi import FastAPI
from . import api, handlers
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
        {"name": "Users", "description": "Operations related to user accounts."},
        {"name": "Authentication", "description": "Login and token management."},
        {"name": "Books", "description": "Operations related to books."},
        {"name": "Genres", "description": "Operations related to books' genres."},
    ],
)

handlers.register_exception_handlers(app)

## === ROUTERS ===
app.include_router(api.book_router)
app.include_router(api.user_router)
app.include_router(api.genre_router)
