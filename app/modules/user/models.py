import datetime
from typing import List

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.modules.training.models import Workout


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)

    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    workouts: Mapped[List["Workout"]] = relationship(back_populates="user", cascade="all, delete-orphan")

