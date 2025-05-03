from fastapi import APIRouter

book_router = APIRouter()

@book_router.get("/books", tags=["Books"])
async def get_books():
    return {"books": "No books yet"}