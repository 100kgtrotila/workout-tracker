from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError
from app.core.security import verify_password, DUMMY_HASH, get_password_hash
from app.modules.user.models import User
from app.modules.user.schemas import UserCreate


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> Optional[User]:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user:
        verify_password(password, DUMMY_HASH)
        return None

    if not verify_password(password, db_user.password_hash):
        return None

    return db_user


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    query = select(User).where(User.email == user_data.email)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise BadRequestError("This email address is already registered.")

    hashed_password = get_password_hash(user_data.password)

    new_user = User(email=user_data.email, password_hash=hashed_password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user