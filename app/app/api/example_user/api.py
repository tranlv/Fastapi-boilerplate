from typing import Any, List
from datetime import datetime, timedelta
from app.api import deps
from fastapi import APIRouter, Depends, Response
from app import crud
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.user import User
from common.email import send_confirmation_email
from app.schemas import user as schemas
from app.i18n import i18n
from common.utils import send_error, send_result
from app.core.security import (
    encode_auth_token,
    check_password_hash
)

__author__ = ""
__maintainer__ = ""
__email__ = ""
__copyright__ = ""


router = APIRouter()


@router.get("/me", response_model=schemas.FullUser)
def get_current_user_information(
    *,
    current_user: User = Depends(deps.get_logged_user),
) -> Any:
    """
    Get current user information
    """
    return current_user


@router.post("/register", response_model=schemas.FullUser)
def register(
    *,
    db: Session = Depends(deps.get_db),
    payload: schemas.UserRegistrationPayload,
) -> Any:
    user = crud.user.get_by_email(db, email=payload.email)
    if user:
        return send_error(
            code=422, message=i18n.t("validation.error.email_existed")
        )

    user = crud.user.create(db, obj_in=payload)
    # @TODO: fix send mail
    # send_confirmation_email(to=user.email, user=user)
    return schemas.FullUser(**dict(id=user.id))


@router.post("/login")
def login(
    *,
    db: Session = Depends(deps.get_db),
    payload: schemas.EmailPasswordPayload,
    response: Response
) -> Any:
    user = crud.user.authenticate(
        db, email=payload.email, password=payload.password
    )
    # @TODO:
    # record the login attempt to redis to prevent brute-force attack
    if user is None:
        return send_error(
            code=400,
            message=i18n.t("authentication.error.incorrect_email_or_password")
        )

    if user.confirmed is False:
        send_confirmation_email(to=user.email, user=user)
        return send_error(
            code=400,
            message=i18n.t("authentication.error.account_not_existed_or_confirmed")
        )
    auth_token = encode_auth_token(subject=user.id)
    expires_in_sec = int(timedelta(days=7).total_seconds())
    response.set_cookie(
        key=settings.COOKIE_API_KEY,
        value=auth_token,
        secure=True,
        httponly=True,
        expires=expires_in_sec
    )
    return {"message": "OK"}
    # return send_result(data={"access_token": auth_token})


@router.post("/change-password")
def change_password(
    *,
    payload: schemas.ChangePasswordPayload,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_logged_user)
) -> Any:
    if not check_password_hash(
        payload.old_password, current_user.password_hash
    ):
        return send_error(
            code=401,
            message=i18n.t("authentication.error.incorrect_email_or_password")
        )
    current_user = crud.user.set_password(db, current_user, payload.password)
    # @TODO: ask why change password leading to confirm the email???
    if current_user.confirmed is False:
        current_user.confirmed = True
        current_user.email_confirmed_at = datetime.now()
    db.session.commit()
    return send_result()


@router.post("/logout")
def logout(response: Response) -> Any:
    response.delete_cookie(key=settings.COOKIE_API_KEY)
    return {"message": "OK"}
