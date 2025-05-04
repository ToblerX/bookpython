from pydantic import BaseModel
import datetime


class UserModel(BaseModel):
    id: int
    username: str
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(BaseModel):
    username: str
    hashed_password: str
