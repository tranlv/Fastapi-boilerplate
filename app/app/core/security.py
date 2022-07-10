from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from app.i18n import i18n


__author__ = ""
__maintainer__ = ""
__email__ = ""
__copyright__ = ""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def encode_auth_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {
        "exp": expire,
        'iat': datetime.utcnow(),
        'iss': "admin@staging.com",
        "sub": str(subject)
    }
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(
            auth_token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload['sub'], payload['exp'], ''  # return the user_id

    except jwt.ExpiredSignatureError:
        return None, None, i18n.t('authentication.error.token_expired')

    except jwt.InvalidTokenError:
        return None, None, i18n.t('authentication.error.token_invalid')
