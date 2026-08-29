from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.models.base import BaseModel


class Reader(BaseModel, table=True):
    card_no: str = Field(unique=True, nullable=False, min_length=6, max_length=6, regex=r"^\d{6}$")


class CreateReaderSchema(SQLModel):
    card_no: str

    @field_validator("card_no")
    @classmethod
    def validate_card_no(cls, value: str) -> str:
        if len(value) != 6:
            raise ValueError("Card number must contain exactly 6 digits")

        if not value.isdigit():
            raise ValueError("Card number must contain digits only.")

        return value


class ReaderView(SQLModel):
    card_no: str

    # lent_books: str
