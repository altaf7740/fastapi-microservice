from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from ..config.settings import settings
from .logging import RequestIDAndLoggingMiddleware


def register_middlewares(app: FastAPI) -> None:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.APP_ALLOWED_HOSTS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.APP_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDAndLoggingMiddleware)


__all__ = ["register_middlewares"]
