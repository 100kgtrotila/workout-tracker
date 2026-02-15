from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, DUMMY_HASH
from app.modules.user.models import User


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | bool:
    query =select(User).where(User.email==username)
    result = await session.execute(query)

    db_user = result.scalar_one_or_none()

    if not db_user:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, hashed_password=db_user.password_hash):
        return False

    return db_user


