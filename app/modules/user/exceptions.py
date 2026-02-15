from app.core.exceptions import AppError


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Could not validate credentials"):
        self.message = message
        super().__init__(self.message)