from app.core.exceptions import NotFoundError, BadRequestError

class ExerciseNotFoundError(NotFoundError):
    def __init__(self, exercise_id: int):
        super().__init__(f"Exercise with id {exercise_id} not found!")

class ExerciseAlreadyExistsError(BadRequestError):
    def __init__(self, exercise_name: str):
        super().__init__(f"Exercise with name {exercise_name} is already exists")