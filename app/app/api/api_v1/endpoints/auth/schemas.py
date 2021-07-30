from typing import Optional
from common.validator import (
    is_valid_password,
    is_valid_display_name,
    is_valid_email
)
from pydantic import BaseModel, EmailStr, validator


class EmailRegistrationPayload(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    display_name: str
    is_policy_accepted: bool

    @validator('email')
    def validate_email(cls, v):
        if not is_valid_email(v):
            raise ValueError('email is not valid')
        return v

    @validator('display_name')
    def validate_display_name(cls, v):
        if not is_valid_display_name(v):
            raise ValueError('display_name is not valid')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not is_valid_password(v):
            raise ValueError(lambda: 'password is not valid')
        return v

    @validator('password_confirm')
    def validate_password_confirm(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Password do not match")
        return v


class EmailPasswordPayload(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not is_valid_email(v):
            raise ValueError('email is not valid')
        return v
