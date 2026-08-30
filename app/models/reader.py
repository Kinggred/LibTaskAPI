from sqlmodel import Field, SQLModel

from app.models.base import BaseModel
from app.models.common import SixDigitIdentifier


class Reader(BaseModel, table=True):
    card_no: str = Field(unique=True, nullable=False, min_length=6, max_length=6, regex=r"^\d{6}$")


class CreateReaderSchema(SQLModel):
    card_no: SixDigitIdentifier


class ReaderView(SQLModel):
    card_no: str

    # lent_books: str


class ReaderInBook(SQLModel):
    card_no: SixDigitIdentifier
