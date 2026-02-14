import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)

    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

