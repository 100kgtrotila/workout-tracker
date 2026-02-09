from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.modules.exercise.enums import MuscleGroup


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500))

    muscle_group: Mapped[MuscleGroup] = mapped_column(SQLEnum(MuscleGroup))