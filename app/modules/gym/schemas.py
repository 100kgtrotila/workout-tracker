from typing import Optional
from pydantic import Field

from app.core.schemas import CustomModel
from app.modules.gym.enums import MuscleGroup

class ExerciseBase(CustomModel):
    name: str = Field(..., min_length=3, max_length=150, description="Exercise Name")
    description: Optional[str] = Field(
        default=None, min_length=10, max_length=1000, description="Exercise description"
    )
    muscle_group: MuscleGroup


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(CustomModel):
    name: Optional[str] = Field(
        default=None, min_length=3, max_length=150, description="Exercise Name"
    )
    description: Optional[str] = Field(
        default=None, min_length=10, max_length=1000, description="Exercise description"
    )
    muscle_group: Optional[MuscleGroup] = None


class ExerciseResponse(ExerciseBase):
    id: int