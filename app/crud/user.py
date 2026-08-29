from sqlmodel import Session, select

from app.crud.base import CRUDBase
from app.models.user import User, UserCreate, UserCreateSchema, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    def get_user_by_email(db: Session, *, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    def create_user(self, db: Session, *, user: UserCreateSchema, pwd_hash) -> User:
        db_user = UserCreate(
            **user.model_dump(exclude={"password"}),
            password_hash=pwd_hash,
        )
        return self.create(db, obj_in=db_user)


crud_user = CRUDUser(User)
