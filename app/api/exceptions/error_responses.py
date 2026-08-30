from sqlmodel import SQLModel


class ErrorResponse(SQLModel):
    detail: str


class ValidationErrorResponse(ErrorResponse):
    field: str


VALIDATION_ERROR_RESPONSE = {
    422: {
        "model": ValidationErrorResponse,
        "description": "Validation error",
    }
}

CONFLICTING_VALUE_PROVIDED = {
    409: {
        "model": ErrorResponse,
        "description": "Provided value already exists",
    }
}

REQUESTED_RESOURCE_NOT_FOUND = {
    404: {
        "model": ErrorResponse,
        "description": "Resource not found",
    }
}
