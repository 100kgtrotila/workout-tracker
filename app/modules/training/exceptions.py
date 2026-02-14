from app.core.exceptions import BadRequestError, NotFoundError

class WorkoutNotFoundError(NotFoundError):
    def __init__(self, workout_id: int):
        super().__init__(f"Workout with id {workout_id} not found")


class WorkoutExerciseNotFoundError(NotFoundError):
    def __init__(self, workout_exercise_id: int):
        super().__init__(f"Workout Exercise with id {workout_exercise_id} not found!")


class WorkoutSetNotFoundError(NotFoundError):
    def __init__(self, workoutset_id: int):
        super().__init__(f"Workout set with id {workoutset_id} not found")



class WorkoutAlreadyCompleted(BadRequestError):
    def __init__(self, exercise_name: str):
        super().__init__(f"Workout {exercise_name} is already completed")
