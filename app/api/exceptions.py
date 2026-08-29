from fastapi import status
from fastapi.exceptions import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, message: str | None = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Requested resource not found")


class DatabaseException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


class BadRequestException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")
