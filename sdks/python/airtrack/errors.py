class AirtrackError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class UnauthorizedError(AirtrackError):
    pass


class NotFoundError(AirtrackError):
    pass


class RateLimitError(AirtrackError):
    pass


class ValidationError(AirtrackError):
    pass
