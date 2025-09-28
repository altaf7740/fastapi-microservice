from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from ..config.settings import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        response: Response = await call_next(request)

        content_security_policy = (
            "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;"
            if settings.ENV.lower() in ["dev", "development"]
            else "default-src 'self'"
        )

        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "no-referrer",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": content_security_policy,
        }

        for k, v in headers.items():
            response.headers[k] = v
        return response
