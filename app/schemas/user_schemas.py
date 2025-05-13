from typing import Optional
from pydantic import BaseModel, EmailStr
import datetime


class UserModel(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    disabled: bool
    verified: bool
    role: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInDb(UserModel):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str


class UserDecode(BaseModel):
    username: str


class UserOut(UserDecode):
    id: int
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
