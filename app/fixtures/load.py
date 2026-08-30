from sqlalchemy import create_engine
from sqlmodel import Session, select

from app.core.database import settings
from app.fixtures.data import BOOKS, BORROWS, READERS
from app.models.book import Book
from app.models.borrow_record import BorrowRecord
from app.models.common import BookState
from app.models.reader import Reader


def load_readers(db: Session) -> None:
    for fixture in READERS:
        reader = db.exec(select(Reader).where(Reader.card_no == fixture["card_no"])).one_or_none()

        if reader is not None:
            continue

        db.add(
            Reader(
                card_no=fixture["card_no"],
            )
        )

    db.flush()


def load_books(db: Session) -> None:
    for fixture in BOOKS:
        book = db.exec(select(Book).where(Book.serial == fixture["serial"])).one_or_none()

        if book is not None:
            continue

        db.add(
            Book(
                serial=fixture["serial"],
                title=fixture["title"],
                author=fixture["author"],
                state=fixture["state"],
            )
        )

    db.flush()


def load_borrows(db: Session) -> None:
    for fixture in BORROWS:
        book = db.exec(select(Book).where(Book.serial == fixture["book_serial"])).one()

        reader = db.exec(select(Reader).where(Reader.card_no == fixture["reader_card_no"])).one()

        existing_borrow = db.exec(
            select(BorrowRecord).where(
                BorrowRecord.book_id == book.id,
                BorrowRecord.enabled.is_(True),
            )
        ).one_or_none()

        if existing_borrow is not None:
            continue

        borrow_record = BorrowRecord(
            book_id=book.id,
            reader_id=reader.id,
        )

        db.add(borrow_record)

        book.state = BookState.BORROWED
        db.add(book)

    db.flush()


def load_fixtures() -> None:
    print("Loading demo fixtures...")
    engine = create_engine(settings.POSTGRES_DSN.encoded_string())
    with Session(engine) as db:
        try:
            load_readers(db)
            load_books(db)
            load_borrows(db)

            db.commit()

        except Exception:
            db.rollback()
            raise

    print("Demo fixtures loaded.")


if __name__ == "__main__":
    load_fixtures()
