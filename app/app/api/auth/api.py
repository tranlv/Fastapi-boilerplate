from typing import Any, List
from datetime import datetime
from app.api import deps
from fastapi import APIRouter, Depends
from app.schemas import user as schemas
from app.crud import user as crud
from sqlalchemy.orm import Session
from app.models.auth import UserBan, User
from common.email import send_confirmation_email
from app.schemas import response
from app.i18n import i18n
from common.utils import send_error, send_result
from app.core.security import (
    encode_auth_token,
    check_password_hash
)


router = APIRouter()


@router.post("/register", response_model=response.SuccessMessageResponse)
def register(
    *,
    db: Session = Depends(deps.get_db),
    payload: schemas.EmailRegistrationPayload,
) -> Any:
    user = crud.user.get_by_display_name(db, display_name=payload.display_name)
    if user:
        return send_error(
            code=422, message=i18n.t("validation.error.display_name_existed")
        )

    banned = db.query(UserBan).filter(UserBan.ban_by == payload.email).first()
    if banned:
        return send_error(
            code=400, message=i18n.t("authentication.error.account_banned")
        )

    # @TODO: ask why we accept duplicate email here
    # if we send confirm email, how do people know their password?
    user = crud.user.get_by_email(db, email=payload.email)
    if user:
        if user.confirmed is False:
            send_confirmation_email(to=user.email, user=user)
        return send_result()

    user = crud.user.create(db, obj_in=payload)
    send_confirmation_email(to=user.email, user=user)
    return user


@router.post("/login")
def login(
    *,
    db: Session = Depends(deps.get_db),
    payload: schemas.EmailPasswordPayload
) -> Any:
    banned = db.query(UserBan).filter(UserBan.ban_by == payload.email).first()
    if banned:
        return send_error(
            code=400,
            message=i18n.t("authentication.error.account_banned")
        )

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
    user.is_deactivated = False
    db.commit()
    auth_token = encode_auth_token(subject=user.id)
    return send_result(data={"access_token": auth_token.decode("utf-8")})


@router.post("/confirm")
def confirm() -> Any:
    pass


@router.post("/password-reset-email")
def password_reset_email() -> Any:
    pass


@router.post("/password-reset-email-confirm")
def password_reset_email_confirm() -> Any:
    pass


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


@router.post("/social_login/google")
def social_login_google() -> Any:
    pass


@router.post("/social_login/facebook")
def social_login_facebook() -> Any:
    pass


@router.post("/sms/register")
def register_sms() -> Any:
    pass


@router.post("/sms/confirm")
def register_sms_confirm() -> Any:
    pass


@router.post("/sms/login_password")
def login_sms_password() -> Any:
    pass


@router.post("/sms/login_code")
def sms_login_code() -> Any:
    pass


@router.post("/sms/login_code/confirm")
def sms_login_code_confirm() -> Any:
    pass


@router.post("/password-reset-phone")
def password_reset_phone() -> Any:
    pass


@router.post(
    "/password-reset-phone-confirm"
)
def password_reset_phone_confirm() -> Any:
    pass


@router.post("/change-phone-number")
def change_phone_number() -> Any:
    pass


@router.post("/send-OTP")
def send_otp() -> Any:
    pass


@router.post("/change-password-token")
def change_password_token() -> Any:
    pass


@router.post("/logout")
def logout() -> Any:
    pass
