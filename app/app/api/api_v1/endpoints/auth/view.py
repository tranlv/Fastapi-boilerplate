from typing import Any, List
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException
from app.api.api_v1.endpoints.auth import schemas
from app.api.api_v1.endpoints.auth import crud
from sqlalchemy.orm import Session
from app.models.auth import UserBan
from common.email import send_confirmation_email
from app.schemas import response

router = APIRouter()


@router.post("/register", response_model=response.SuccessMessageResponse)
def register(
    *,
    db: Session = Depends(deps.get_db),
    payload: schemas.EmailRegistrationPayload,
) -> Any:
    user = crud.user.get_by_display_name(db, display_name=payload.display_name)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this display_name already exists in the system.",
        )
    banned = db.query(UserBan).filter(UserBan.ban_by == payload.email).first()
    if banned:
        raise HTTPException(
            status_code=400,
            detail="The user has been banned",
        )

    # @TODO: ask why we accept duplicate email here
    # if we send confirm email, how do people know their password?
    user = crud.user.get_by_email(db, email=payload.email)
    if user:
        if user.confirmed is False:
            send_confirmation_email(to=user.email, user=user)
        return {"message": "success"}

    user = crud.user.create(db, obj_in=payload)
    send_confirmation_email(to=user.email, user=user)
    return user


@router.post("/login")
def login() -> Any:
    pass


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
def change_password() -> Any:
    pass


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
