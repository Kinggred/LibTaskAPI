from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.exceptions.exceptions import APIException


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        APIException,
        api_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )


async def api_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if not isinstance(exc, APIException):
        raise exc

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        raise exc

    error = exc.errors()[0]

    message = error["msg"].removeprefix("Value error, ")


    loc = error["loc"]
    field = str(loc[-1])

    return JSONResponse(
        status_code=422,
        content={
            "detail": message,
            "fields": field,
        },
    )
