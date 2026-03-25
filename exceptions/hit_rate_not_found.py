from exceptions.custom_exception import CustomException

class HitRateNotFoundException(CustomException):
    """Exception raised when hit rate data is not found."""
    def __init__(self, message: str = "No Available Data for this particular sport at this time.", status_code: int = 404):
        super().__init__(message, status_code)