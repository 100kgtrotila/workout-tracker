from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from app.modules.gym.enums import MuscleGroup
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.training.models import WorkoutExercise

class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    muscle_group: Mapped[MuscleGroup] = mapped_column(SQLEnum(MuscleGroup))

    workout_exercises: Mapped[List["WorkoutExercise"]] = relationship(back_populates="exercise")