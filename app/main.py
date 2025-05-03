from fastapi import FastAPI
from .api import book_router, user_router
app = FastAPI(
    title="Book Python API",
    description="API to handle operations in a book shop.",
    version="1.0",
    openapi_tags=[
        {"name": "Users", "description": "Operations related to user accounts."},
        {"name": "Authentication", "description": "Login and token management."},
        {"name": "Books", "description": "Operations related to books."},
    ],
)

app.include_router(book_router)
app.include_router(user_router)