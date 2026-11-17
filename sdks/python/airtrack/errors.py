class AirtrackError(Exception):
    def __init__(self, message: str, status_code: int | None = None, detail=None):
        self.status_code = status_code
        self.detail = detail  # the API's full "detail" (a dict for 409, a list for 422)
        super().__init__(message)


class UnauthorizedError(AirtrackError):
    pass


class ForbiddenError(AirtrackError):
    """For example the plan's shipment limit is reached."""


class NotFoundError(AirtrackError):
    pass


class ConflictError(AirtrackError):
    """The AWB is already tracked; detail["shipment_id"] is the existing shipment."""


class RateLimitError(AirtrackError):
    pass


class ValidationError(AirtrackError):
    pass
