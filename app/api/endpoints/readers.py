from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_pagination import Page
from sqlmodel import Session

from app.api.responses import CONFLICTING_VALUE_PROVIDED, VALIDATION_ERROR_RESPONSE
from app.core.database import get_session
from app.crud.reader import crud_reader
from app.models.reader import CreateReaderSchema, ReaderView

router = APIRouter()


@router.get("/", response_model=Page[ReaderView])
def get_readers(db: Annotated[Session, Depends(get_session)]) -> Page[ReaderView]:
    return crud_reader.paginated_get_all(db=db)


@router.post("/", response_model=ReaderView, responses=VALIDATION_ERROR_RESPONSE | CONFLICTING_VALUE_PROVIDED,)
def create_reader(
    db: Annotated[Session, Depends(get_session)],
    reader: CreateReaderSchema,
) -> ReaderView:
    return crud_reader.create(db=db, obj_in=reader)
