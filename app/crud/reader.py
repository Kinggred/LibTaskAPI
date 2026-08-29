from sqlmodel import Session, select

from app.api.exceptions import ConflictingDataException
from app.crud.base import CRUDBase
from app.models.reader import CreateReaderSchema, Reader


class CRUDReader(CRUDBase[Reader, CreateReaderSchema, CreateReaderSchema]):
    def get_reader_by_card_no(self, db: Session, card_no: str) -> Reader | None:
        statement = select(Reader).where(Reader.card_no == card_no)
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: CreateReaderSchema, **kwargs) -> Reader:
        reader = self.get_reader_by_card_no(db=db, card_no=obj_in.card_no)
        if reader:
            raise ConflictingDataException
        return super().create(db=db, obj_in=obj_in)


crud_reader = CRUDReader(Reader)
