from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.modules.training.enums import WorkoutStatus

if TYPE_CHECKING:
    from app.modules.user.models import User
    from app.modules.gym.models import Exercise

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[WorkoutStatus] = mapped_column(default=WorkoutStatus.PLANNED)
    notes: Mapped[Optional[str]] = mapped_column(String(500))

    user: Mapped["User"] = relationship(back_populates="workouts")

    exercises: Mapped[List["WorkoutExercise"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan"
    )

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    order: Mapped[int] = mapped_column(Integer, default=0)

    workout: Mapped["Workout"] = relationship(back_populates="exercises")
    exercise: Mapped["Exercise"] = relationship(back_populates="workout_exercises")

    sets: Mapped[List["WorkoutSet"]] = relationship(
        back_populates="workout_exercise",
        cascade="all, delete-orphan"
    )

class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_exercise_id: Mapped[int] = mapped_column(ForeignKey("workout_exercises.id"))

    reps: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    set_number: Mapped[int] = mapped_column(Integer)

    workout_exercise: Mapped["WorkoutExercise"] = relationship(back_populates="sets")