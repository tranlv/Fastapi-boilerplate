from fastapi import APIRouter

from . import example_user


api_router = APIRouter()
api_router.include_router(
    example_user.router, prefix="/example_user", tags=["example_user"]
)
