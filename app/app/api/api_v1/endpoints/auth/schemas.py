from datetime import datetime
from typing import Optional
from app.i18n import i18n
from common.validator import (
    is_valid_password,
    is_valid_display_name,
    is_valid_email
)
from pydantic import (
    BaseModel,
    EmailStr,
    validator,
    root_validator
)


class EmailRegistrationPayload(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    display_name: str
    is_policy_accepted: bool

    @validator('email')
    def validate_email(cls, v):
        if not is_valid_email(v):
            raise ValueError(i18n.t("validation.error.invalid_email"))
        return v

    @validator('display_name')
    def validate_display_name(cls, v):
        if not is_valid_display_name(v):
            raise ValueError(i18n.t("validation.error.invalid_display_name"))
        return v

    @validator('password')
    def validate_password(cls, v):
        if not is_valid_password(v):
            raise ValueError(i18n.t("validation.error.invalid_password"))
        return v

    @validator('password_confirm')
    def validate_password_confirm(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError(
                i18n.t("validation.error.password_confirm_not_match")
            )
        return v


class EmailPasswordPayload(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not is_valid_email(v):
            raise ValueError(i18n.t("validation.error.invalid_email"))
        return v


class ChangePasswordPayload(BaseModel):
    old_password: str
    password: str
    password_confirm: str

    @validator('password')
    def validate_password(cls, v):
        if not is_valid_password(v):
            raise ValueError(i18n.t("validation.error.invalid_password"))
        return v

    @validator('password_confirm')
    def validate_password_confirm(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError(
                i18n.t("validation.error.password_confirm_not_match")
            )
        return v


# data to passed when create user
class CreateUserData(BaseModel):
    email: EmailStr
    phone_number: Optional[str]
    password: str
    display_name: str
    confirmed: Optional[bool] = False
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    gender: Optional[str]
    email_confirmed_at: Optional[datetime]
    verification_sms_time: Optional[datetime]

    @root_validator
    def check_phone_or_email(cls, values):
        email, phone_number = values.get('email'), values.get('phone_number')
        if email is None and phone_number is None:
            raise ValueError(
                i18n.t("validation.error.email_or_phone_required")
            )
        return values
