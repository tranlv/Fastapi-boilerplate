
from fastapi import APIRouter

from . import example_user


__author__ = ""
__maintainer__ = ""
__email__ = ""
__copyright__ = ""



api_router = APIRouter()
api_router.include_router(
    example_user.router, prefix="/example_user", tags=["example_user"]
)
