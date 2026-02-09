import enum

class MuscleGroup(str, enum.Enum):
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"
    ARMS = "arms"
    SHOULDERS = "shoulders"
    CARDIO = "cardio"