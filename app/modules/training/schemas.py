from datetime import datetime
from typing import Optional, List

from pydantic import Field

from app.core.schemas import CustomModel
from app.modules.training.enums import WorkoutStatus


# Workout Sets
class WorkoutSetBase(CustomModel):
    reps: int = Field(..., ge=1, description="Number of repetitions")
    weight: float = Field(..., ge=0.0, description="Weight in kg")
    set_number: int = Field(..., ge=1, description="Number of set")

class WorkoutSetCreate(WorkoutSetBase):
    pass

class WorkoutSetUpdate(CustomModel):
    reps: Optional[int] = Field(default=None, ge=1, description="Number of repetitions")
    weight: Optional[float] = Field(default=None, ge=0.0, description="Weight in kg")
    set_number: Optional[int] = Field(default=None, ge=1, description="Number of set")

class WorkoutSetResponse(WorkoutSetBase):
    id: int
    workout_exercise_id: int


# Workout Exercises
class WorkoutExerciseBase(CustomModel):
    exercise_id: int
    order: int = Field(default=0, description="Order of execution")

class WorkoutExerciseCreate(WorkoutExerciseBase):
    sets: List[WorkoutSetCreate] = []

class WorkoutExerciseUpdate(CustomModel):
    order: Optional[int] = Field(default=None, description="Order of execution")

class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: int
    workout_id: int
    sets: List[WorkoutSetResponse] = []


# Workouts
class WorkoutBase(CustomModel):
    name: str = Field(..., min_length=3, max_length=128, description="Workout name")
    scheduled_at: datetime
    notes: Optional[str] = Field(default=None, min_length=10, max_length=256, description="Workout notes")
    status: WorkoutStatus = Field(default=WorkoutStatus.PLANNED)

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate] = []

class WorkoutUpdate(CustomModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=128, description="Workout name")
    scheduled_at: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, min_length=10, max_length=256, description="Workout notes")
    status: Optional[WorkoutStatus] = None

class WorkoutResponse(WorkoutBase):
    id: int
    user_id: int
    exercises: List[WorkoutExerciseResponse] = []