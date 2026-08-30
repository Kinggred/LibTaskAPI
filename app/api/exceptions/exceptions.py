from fastapi import status


class APIException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = "Something went wrong"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class ConflictingDataException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_message = "Provided value already exists"


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Requested resource not found"


class DatabaseException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "Something went wrong"


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Bad request"
