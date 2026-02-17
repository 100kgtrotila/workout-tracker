import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.modules.user.exceptions import UnauthorizedError
from app.modules.user.models import User

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("playboicarti")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise UnauthorizedError("Token username error")

    except InvalidTokenError:
        raise UnauthorizedError("Your token is expired")

    query = select(User).where(User.email == username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedError("User not found")

    return user
