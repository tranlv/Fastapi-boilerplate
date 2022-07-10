from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from app.core.security import (
    check_password_hash,
    generate_password_hash
)
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas import user as schemas
from fastapi.encoders import jsonable_encoder


__author__ = ""
__maintainer__ = ""
__email__ = ""
__copyright__ = ""


class CRUDUser(CRUDBase[User, schemas.CreateUserData, schemas.CreateUserData]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_display_name(
        self, db: Session, *, display_name: str
    ) -> Optional[User]:
        return db.query(User).filter(User.display_name == display_name).first()

    def create(self, db: Session, *, obj_in: schemas.CreateUserData) -> User:
        obj_in_data = jsonable_encoder(obj_in)

        # @TODO: this is hardcode
        if "password" in obj_in_data:
            del obj_in_data["password"]
            del obj_in_data["password_confirm"]

        db_obj = self.model(
            **obj_in_data,
            password_hash=generate_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self,
        db: Session,
        *,
        email: str,
        password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not check_password_hash(user.password_hash, password):
            return None
        return user

    def set_password(self, db: Session, user, password):
        user.password_hash = generate_password_hash(password)
        return user


user = CRUDUser(User)
