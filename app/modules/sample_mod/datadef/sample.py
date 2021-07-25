from marshmallow import Schema, fields, ValidationError, INCLUDE
from app.extensions.utils import messages
from app.extensions.utils.util import (
    is_valid_password,
    is_valid_display_name,
    is_valid_phone_number
)
from app.extensions.schema import HoovadaSchema


def validate_password(data):
    if not is_valid_password(data):
        raise ValidationError(messages.ERR_INVALID_PASSWORD)


def validate_display_name(data):
    if not is_valid_display_name(data):
        raise ValidationError(messages.ERR_INVALID_DISPLAY_NAME)


class EmailRegistrationSchema(HoovadaSchema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": messages.ERR_PLEASE_PROVIDE.format('email')
        },
        metadata={"description": "The email used for registration"}
    )
    password = fields.Str(
        required=True,
        validate=validate_password,
        error_messages={
            "required": messages.ERR_PLEASE_PROVIDE.format('password')
        }
    )
    password_confirm = fields.Str(
        required=True,
        validate=validate_password,
        error_messages={
            "required": messages.ERR_PLEASE_PROVIDE.format('password_confirm')
        }
    )
    display_name = fields.Str(
        required=True,
        validate=validate_display_name,
        error_messages={
            "required": messages.ERR_PLEASE_PROVIDE.format('display_name')
        }
    )
    is_policy_accepted = fields.Bool(
        required=True,
        error_messages={
            "required": messages.ERR_NO_POLICY_ACCEPTED
        }
    )

    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE
