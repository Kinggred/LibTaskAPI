from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.base import BaseModel
from app.models.common import SixDigitIdentifier
from app.models.reader import Reader


class BorrowRecord(BaseModel, table=True):
    book_id: UUID = Field(
        foreign_key="book.id",
        nullable=False,
        index=True,
    )

    reader_id: UUID = Field(
        foreign_key="reader.id",
        nullable=False,
        index=True,
    )
class CreateBorrowRecord(SQLModel):
    book_id: UUID
    reader_id: UUID


class CreateBorrowRecordSchema(SQLModel):
    reader_card_no: SixDigitIdentifier

class BorrowRecordView(SQLModel):
    reader_card_no: SixDigitIdentifier
    borrowed_at: datetime

    @classmethod
    def from_models(
        cls,
        borrow_record: BorrowRecord,
        reader: Reader,
    ) -> BorrowRecordView:
        return cls(
            reader_card_no=reader.card_no,
            borrowed_at=borrow_record.created_at,
        )
