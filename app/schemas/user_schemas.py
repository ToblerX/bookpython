from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator
import datetime, re
from app import config, schemas
from app.exceptions import errors


class UserModel(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    disabled: bool
    verified: bool
    role: str
    wishlist: Optional[List[schemas.BookOut]] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class UserInDb(UserModel):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < config.USERNAME_MIN or len(value) > config.USERNAME_MAX:
            raise errors.IncorrectUsernameLength()
        return value

    @field_validator("hashed_password")
    def validate_password(cls, value):
        if len(value) < config.PASSWORD_MIN or len(value) > config.PASSWORD_MAX:
            raise errors.IncorrectPasswordLength()
        if not re.search(r"[A-Z]", value) or not re.search(
            r'[!@#$%^&*(),.?":{}|<>]', value
        ):
            raise errors.IncorrectPasswordFormat()
        return value


class UserDecode(BaseModel):
    user_id: int
    username: str


class UserOut(UserDecode):
    id: int
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class PasswordResetRequestModel(BaseModel):
    email: EmailStr


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
