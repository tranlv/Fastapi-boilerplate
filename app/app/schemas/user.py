from datetime import datetime
from typing import Optional
from app.i18n import i18n
from common.validator import (
    is_valid_password,
    is_valid_email
)
from pydantic import (
    BaseModel,
    EmailStr,
    validator
)


class UserRegistrationPayload(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    first_name: str
    last_name: str
    gender: str
    birthday: datetime

    @validator('password')
    def validate_password(cls, v):
        if not is_valid_password(v):
            raise ValueError(i18n.t("validation.error.invalid_password"))
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['M', 'F', 'U', 'O']:
            raise ValueError(i18n.t("validation.error.invalid_gender"))
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


class UpdateUserPayload(BaseModel):
    username: Optional[str]
    phone_number: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]
    email: Optional[str]
    avatar: Optional[str]


# data to passed when create user
class CreateUserData(UpdateUserPayload):
    last_seen: Optional[datetime]
    joined_date: Optional[datetime]
    confirmed: Optional[bool]
    confirmed_at: Optional[datetime]


class FullUser(CreateUserData):
    id: int

    class Config:
        orm_mode = True
