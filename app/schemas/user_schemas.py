from typing import Optional

from pydantic import BaseModel
import datetime


class UserModel(BaseModel):
    user_id: int
    username: str
    disabled: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInDb(UserModel):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class UserDecode(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
