
from sqlmodel import Session, select

from app.api.exceptions.exceptions import ConflictingDataException, NotFoundException
from app.crud.base import CRUDBase
from app.models.book import Book, CreateBookSchema, UpdateBookSchema
from app.models.common import BookState, SixDigitIdentifier


class CRUDBook(CRUDBase[Book, CreateBookSchema, UpdateBookSchema]):
    def get_book_by_serial(
        self, db: Session, *, serial: SixDigitIdentifier, include_removed: bool = False
    ) -> Book | None:
        statement = select(Book).where(Book.serial == serial)

        if not include_removed:
            statement = statement.where(Book.enabled == True)
        return db.exec(statement).one_or_none()

    def create(self, db: Session, *, obj_in: CreateBookSchema, **kwargs) -> Book:
        book = self.get_book_by_serial(db=db, serial=obj_in.serial, include_removed=True)
        if book:
            if not book.enabled:
                raise ConflictingDataException("Reenabling of a record is not yet supported")
            raise ConflictingDataException
        return super().create(db=db, obj_in=obj_in, **kwargs)

    def change_book_state(self, db: Session, *, serial: SixDigitIdentifier, new_state: BookState) -> Book:
        book = self.get_book_by_serial(db=db, serial=serial)
        if not book:
            raise NotFoundException(message="Book not found")

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
