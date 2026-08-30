from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.base import BaseModel
from app.models.common import BookState, SixDigitIdentifier
from app.models.reader import ReaderInBook


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

    borrower: ReaderInBook | None = None
