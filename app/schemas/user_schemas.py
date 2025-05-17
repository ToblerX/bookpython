from typing import Optional
from pydantic import BaseModel, EmailStr, validator
import datetime, re
from app import errors


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

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 5 or len(value) > 15:
            raise errors.IncorrectUsernameLength()
        return value

    @validator("hashed_password")
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 16:
            raise errors.IncorrectPasswordLength()
        if not re.search(r"[A-Z]", value) or not re.search(
            r'[!@#$%^&*(),.?":{}|<>]', value
        ):
            raise errors.IncorrectPasswordFormat()
        return value


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
