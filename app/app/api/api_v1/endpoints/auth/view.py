from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from app.api.api_v1.endpoints.auth import schemas

router = APIRouter()


@router.post("/register")
def register(payload: schemas.EmailRegistrationPayload) -> Any:
    return payload


@router.post("/login")
def login() -> Any:
    pass


@router.post("/confirm")
def confirm() -> Any:
    pass


@router.post("/password-reset-email")
def password_reset_email() -> Any:
    pass


@router.post(
    "/password-reset-email-confirm"
)
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
