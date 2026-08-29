
from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models.reader import CreateReaderSchema, Reader


class CRUDReader(CRUDBase[Reader, CreateReaderSchema, CreateReaderSchema]):
    def get_reader_by_card_no(self, db: Session, card_no: str) -> Reader | None:
        statement = select(Reader).where(Reader.card_no == card_no)
        return db.exec(statement).first()


crud_reader = CRUDReader(Reader)

