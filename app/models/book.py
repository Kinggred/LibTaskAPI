from datetime import datetime
from typing import Any

from sqlmodel import Field, SQLModel

from app.models.base import BaseModel
from app.models.borrow_record import BorrowRecord, BorrowRecordView
from app.models.common import BookState, SixDigitIdentifier
from app.models.reader import Reader


class Book(BaseModel, table=True):
    serial: str = Field(unique=True, nullable=False, min_length=6, max_length=6, regex=r"^\d{6}$")
    title: str
    author: str
    state: BookState


class CreateBookSchema(SQLModel):
    serial: SixDigitIdentifier
    title: str
    author: str
    state: BookState = BookState.AVAILABLE


class UpdateBookSchema(SQLModel):
    title: str
    author: str


class BookView(SQLModel):
    serial: SixDigitIdentifier
    title: str
    author: str
    state: BookState
    created_at: datetime
    updated_at: datetime


class BookExtendedView(BookView):
    borrow_record: BorrowRecordView | None

    @classmethod
    def transformer(cls, rows) -> list[BookExtendedView]:
        return [BookExtendedView.from_row(row) for row in rows]

    @classmethod
    def from_row(cls, row: Any) -> BookExtendedView:
        book, borrow_record, reader = row

        return cls.from_models(
            book=book,
            borrow_record=borrow_record,
            reader=reader,
        )

    @classmethod
    def from_models(
        cls,
        book: Book,
        borrow_record: BorrowRecord | None,
        reader: Reader | None,
    ) -> BookExtendedView:
        return cls(
            **book.model_dump(),
            borrow_record=(
                BorrowRecordView.from_models(
                    borrow_record,
                    reader,
                )
                if borrow_record is not None and reader is not None
                else None
            ),
        )
