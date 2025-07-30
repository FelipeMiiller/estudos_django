
class InvalidUuidException(Exception):
    """Exception raised when an invalid UUID is provided."""
    def __init__(self, message: str = 'ID must be a valid UUID') -> None:
        super().__init__(message)


class InvalidDateException(Exception):
    """Exception raised when an invalid date is provided."""
    def __init__(self, message: str = 'Date must be a valid date') -> None:
        super().__init__(message)
    