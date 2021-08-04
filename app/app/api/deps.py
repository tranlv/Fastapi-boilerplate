from typing import Generator
from datetime import datetime

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.core.security import decode_auth_token
from app.core.config import settings
from app.db.session import SessionLocal
from app.api.api_v1.endpoints.auth import crud
from app.i18n import i18n


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_logged_user(
    request: Request,
    db: Session = Depends(get_db)
) -> models.auth.User:
    auth_token = None
    api_key = None

    if 'X-API-KEY' in request.headers:
        api_key = request.headers['X-API-KEY']

    if 'Authorization' in request.headers:
        auth_token = request.headers.get('Authorization')

    if not auth_token and not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=i18n.t('authentication.error.missing_token')
        )

    if api_key is not None:
        auth_token = api_key

    user_id, expiration, message = decode_auth_token(auth_token=auth_token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )

    # @TODO: wire redis and handle blacklist token
    # blacklist_token = redis_client.get(get_blacklist_token_key(auth_token))
    # if blacklist_token is not None:
    #     return None, 'Unauthorized'

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=i18n.t('authentication.error.user_not_found')
        )
    user.last_seen = datetime.now()
    db.commit()
    return user
