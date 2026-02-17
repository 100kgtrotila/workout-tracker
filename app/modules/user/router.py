from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.db import get_db
from app.core.security import create_access_token
from app.modules.user import service
from app.modules.user.exceptions import UnauthorizedError
from app.modules.user.schemas import UserResponse, UserCreate, Token

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
   return await service.create_user(session, user_data)

@router.post("/login", response_model=Token)
async def login_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_db)):

    user = await service.authenticate_user(session, form_data.email, form_data.password)

    if not user:
        raise UnauthorizedError("Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")