from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.modules.workout.enums import WorkoutStatus


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[id] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(120))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[WorkoutStatus] = mapped_column(default=WorkoutStatus.PLANNED)
    notes: Mapped[Optional[str]] = mapped_column(String(500))

    user: Mapped["User"] = relationship(back_populates="workouts")

    #exercises: Mapped[List[WorkoutExercise]]