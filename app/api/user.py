from fastapi import APIRouter

user_router = APIRouter()


@user_router.get("/users", tags=["Users"])
async def get_users():
    return {"users": "No users yet"}
