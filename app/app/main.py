from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.api.routes import api_router
from app.core.config import settings
from common.utils import request_validation_exception_handler
from app.i18n import configure_i18n

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    exception_handlers={
        RequestValidationError: request_validation_exception_handler
    }
)


@app.middleware("http")
async def set_language(request: Request, call_next):
    language_setting = request.query_params.get(
        'language', settings.I18N_DEFAULT_LANGUAGE
    )
    configure_i18n(settings.I18N_TRANSLATION_PATH, language_setting)
    return await call_next(request)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
