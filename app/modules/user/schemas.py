from dataclasses import Field
from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, EmailStr, BaseModel

from app.core.schemas import CustomModel

class UserBase(CustomModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_lenght=6, max_lenght=128, description="User password")

class UserUpdate(UserBase):
    email: Optional[EmailStr]
    password: Optional[str]

class UserResponse(CustomModel):
    id: PositiveInt
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None