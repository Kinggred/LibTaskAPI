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
from app.models.book import BookExtendedView, BookView, CreateBookSchema
from app.models.borrow_record import CreateBorrowRecordSchema
from app.models.common import BookState, SixDigitIdentifier

router = APIRouter()


@router.get("/", response_model=Page[BookExtendedView])
def get_books(db: Annotated[Session, Depends(get_session)]) -> Page[BookExtendedView]:
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

@router.delete("/{serial}", responses=VALIDATION_ERROR_RESPONSE)
def delete_book(db: Annotated[Session, Depends(get_session)], serial: SixDigitIdentifier) -> None:
    crud_book.safe_remove(db=db, serial=serial)

@router.post("/{serial}/borrow", response_model=BookView, responses=VALIDATION_ERROR_RESPONSE)
def borrow_book(db: Annotated[Session, Depends(get_session)], serial: SixDigitIdentifier, body: CreateBorrowRecordSchema) -> BookView:
    return crud_book.record_borrow(db=db, serial=serial, reader_card_no=body.reader_card_no)

@router.delete("/{serial}/borrow", response_model=BookView, responses=VALIDATION_ERROR_RESPONSE)
def return_book(db: Annotated[Session, Depends(get_session)], serial: SixDigitIdentifier) -> BookView:
    return crud_book.record_return(db=db, serial=serial)