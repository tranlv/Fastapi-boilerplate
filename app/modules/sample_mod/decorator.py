from functools import wraps
from marshmallow import ValidationError
from app.extensions.utils.response import send_error
from app.extensions.utils import messages

def validate_payload(schema_cls):

    def inner(f):
        @wraps(f)
        def decorated(self, data, *args, **kwargs):
            if not isinstance(data, dict):
                return send_error(message=messages.ERR_WRONG_DATA_FORMAT)

            try:
                validated_data = schema_cls().load(data)
            except ValidationError as err:
                return send_error(message=err.messages)

            return f(self, validated_data, *args, **kwargs)
        return decorated
    return inner
