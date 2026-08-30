from uuid import UUID

from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models.borrow_record import BorrowRecord, CreateBorrowRecord


class CRUDBorrowRecord(CRUDBase[BorrowRecord, CreateBorrowRecord, CreateBorrowRecord]):
    def get_by_book_id(self, db: Session, book_id: UUID) -> BorrowRecord:
        statement = select(BorrowRecord).where(BorrowRecord.book_id == book_id, BorrowRecord.enabled == True)
        return db.exec(statement).one()


crud_borrow_record = CRUDBorrowRecord(BorrowRecord)
