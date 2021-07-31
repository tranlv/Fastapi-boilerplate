from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from datetime import datetime
from app.core.security import (
    check_password_hash,
    generate_password_hash
)
from app.crud.base import CRUDBase
from app.models.auth import User
from app.api.api_v1.endpoints.auth import schemas


class CRUDUser(CRUDBase[User, schemas.CreateUserData, schemas.CreateUserData]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_display_name(
        self, db: Session, *, display_name: str
    ) -> Optional[User]:
        return db.query(User).filter(User.display_name == display_name).first()

    def create(self, db: Session, *, obj_in: schemas.CreateUserData) -> User:
        if isinstance(obj_in, dict):
            obj_in = schemas.CreateUserData(**obj_in)
        else:
            obj_in = schemas.CreateUserData(**dict(obj_in))

        db_obj = User(
            display_name=obj_in.display_name,
            email=obj_in.email,
            confirmed=obj_in.confirmed,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            middle_name=obj_in.middle_name,
            gender=obj_in.gender,
            password_hash=generate_password_hash(obj_in.password),
        )

        if (obj_in.email is not None) and (obj_in.confirmed is True):
            db_obj.email_confirmed_at = datetime.now()

        if obj_in.phone_number is not None and obj_in.confirmed is True:
            db_obj.verification_sms_time = datetime.now()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not check_password_hash(password, user.password_hash):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
