from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_pagination import Page
from sqlmodel import Session

from app.api.exceptions.error_responses import (
    CONFLICTING_VALUE_PROVIDED,
    REQUESTED_RESOURCE_NOT_FOUND,
    VALIDATION_ERROR_RESPONSE,
)
from app.core.database import get_session
from app.crud.book import crud_book
from app.models.book import BookView, CreateBookSchema
from app.models.common import BookState, SixDigitIdentifier

router = APIRouter()


@router.get("/", response_model=Page[BookView])
def get_books(db: Annotated[Session, Depends(get_session)]) -> Page[BookView]:
    return crud_book.paginated_get_all(db=db)


@router.post(
    "/",
    response_model=BookView,
    responses=VALIDATION_ERROR_RESPONSE | CONFLICTING_VALUE_PROVIDED | REQUESTED_RESOURCE_NOT_FOUND,
)
def create_book(db: Annotated[Session, Depends(get_session)], book: CreateBookSchema) -> BookView:
    return crud_book.create(db=db, obj_in=book)


@router.get("/{serial}", response_model=BookView)
def get_book(db: Annotated[Session, Depends(get_session)], serial: SixDigitIdentifier) -> BookView:
    return crud_book.get_book_by_serial(db=db, serial=serial)


@router.patch(
    "/{serial}",
    response_model=BookView,
    responses=VALIDATION_ERROR_RESPONSE | CONFLICTING_VALUE_PROVIDED | REQUESTED_RESOURCE_NOT_FOUND,
)
def update_book_state(
    db: Annotated[Session, Depends(get_session)], serial: SixDigitIdentifier, book_state: BookState
) -> BookView:
    return crud_book.change_book_state(db=db, serial=serial, new_state=book_state)

@router.delete("/{serial}", responses=VALIDATION_ERROR_RESPONSE)
def delete_book(db: Annotated[Session, Depends(get_session)], serial: SixDigitIdentifier) -> None:
    crud_book.safe_remove(db=db, serial=serial)