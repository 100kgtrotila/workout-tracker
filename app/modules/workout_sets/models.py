from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.core.db import Base
from app.modules.workout_exercises.models import WorkoutExercise


class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_exercise_id: Mapped[int] = mapped_column(ForeignKey("workout_exercises.id"))

    reps: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    set_number: Mapped[int] = mapped_column(Integer)

    workout_exercise: Mapped["WorkoutExercise"] = relationship(back_populates="sets")
