import enum

class WorkoutStatus(str, enum.Enum):
    PLANNED = "planned"
    COMPLETED = "completed"
    SKIPPED = "skipped"

