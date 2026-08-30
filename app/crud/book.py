from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, and_, select

from app.api.exceptions.exceptions import ConflictingDataException, NotFoundException
from app.crud.base import CRUDBase
from app.crud.borrow import crud_borrow_record
from app.crud.reader import crud_reader
from app.models.book import Book, BookExtendedView, CreateBookSchema, UpdateBookSchema
from app.models.borrow_record import BorrowRecord, CreateBorrowRecord
from app.models.common import BookState, SixDigitIdentifier
from app.models.reader import Reader


class CRUDBook(CRUDBase[Book, CreateBookSchema, UpdateBookSchema]):
    def get_book_by_serial(
        self, db: Session, *, serial: SixDigitIdentifier, include_removed: bool = False
    ) -> Book | None:
        statement = select(Book).where(Book.serial == serial)

        if not include_removed:
            statement = statement.where(Book.enabled == True)
        return db.exec(statement).one_or_none()

    def paginated_get_all(self, db: Session) -> Page[BookExtendedView]:
        statement = (
            select(Book, BorrowRecord, Reader)
            .outerjoin(
                BorrowRecord,
                and_(BorrowRecord.book_id == Book.id, BorrowRecord.enabled == True),
            )
            .outerjoin(
                Reader,
                and_(Reader.id == BorrowRecord.reader_id, Reader.enabled == True),
            )
            .where(Book.enabled == True)
            .order_by(Book.created_at)
        )

        return paginate(session=db, query=statement, transformer=BookExtendedView.transformer)

    def create(self, db: Session, *, obj_in: CreateBookSchema, **kwargs) -> Book:
        book = self.get_book_by_serial(db=db, serial=obj_in.serial, include_removed=True)
        if book:
            if not book.enabled:
                raise ConflictingDataException("Reenabling of a record is not yet supported")
            raise ConflictingDataException
        return super().create(db=db, obj_in=obj_in, **kwargs)

    def record_borrow(self, db: Session, *, serial: SixDigitIdentifier, reader_card_no: SixDigitIdentifier) -> Book:
        book = self.get_book_by_serial(db=db, serial=serial)
        reader = crud_reader.get_reader_by_card_no(db=db, card_no=reader_card_no)

        if not book:
            raise NotFoundException(message="Book not found")

        if not reader:
            raise NotFoundException(message="Reader not found")

        borrow_record = CreateBorrowRecord(
            book_id=book.id,
            reader_id=reader.id,
        )

        if book.state == BookState.BORROWED:
            raise ConflictingDataException(message="Book not available")
        book.state = BookState.BORROWED

        # This could be problematic if one of the operations fail.
        crud_borrow_record.create(db=db, obj_in=borrow_record)
        return self.db_add_operation(db=db, object_to_add=book)

    def record_return(self, db: Session, *, serial: SixDigitIdentifier) -> Book:
        book = self.get_book_by_serial(db=db, serial=serial)
        if not book:
            raise NotFoundException(message="Book not found")

        # This could be problematic if one of the operations fail.
        borrow_record = crud_borrow_record.get_by_book_id(db=db, book_id=book.id)
        crud_borrow_record.remove(db=db, db_obj=borrow_record)
        book.state = BookState.AVAILABLE
        return self.db_add_operation(db=db, object_to_add=book)

    def change_book_state(self, db: Session, *, book: Book, new_state: BookState) -> Book:
        book.state = new_state
        return self.db_add_operation(db=db, object_to_add=book)

    def safe_remove(
        self,
        db: Session,
        *,
        serial: SixDigitIdentifier,
        hard: bool = False,
    ) -> None:
        book = self.get_book_by_serial(db=db, serial=serial, include_removed=True)
        # TODO: END borrow upon deleting
        if not book:
            raise NotFoundException(message="Book not found")

        super().remove(db=db, db_obj=book)


crud_book = CRUDBook(Book)
