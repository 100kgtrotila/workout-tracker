from email.policy import default

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.core.db import Base


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))

    order: Mapped[int] = mapped_column(Integer, default=1)

    workout: Mapped[int] = relationship(back_populates="exercises")
    exercise: Mapped[int] = relationship(back_populates="workout_exercises")

    