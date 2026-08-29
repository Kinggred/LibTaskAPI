from sqlmodel import SQLModel


class ErrorResponse(SQLModel):
    detail: str

VALIDATION_ERROR_RESPONSE = {
    422: {
        "model": ErrorResponse,
        "description": "Validation error",
    }
}

CONFLICTING_VALUE_PROVIDED = {
    409: {
        "model": ErrorResponse,
        "description": "Provided value already exists",
    }}