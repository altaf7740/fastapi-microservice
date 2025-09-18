import asyncio
from typing import Awaitable, Callable, List

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, timeout: int = 10, exclude_paths: List[str] | None = None) -> None:
        super().__init__(app)
        self.timeout = timeout
        self.exclude_paths = exclude_paths or []

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return Response(
                content='{"detail":"Request timed out"}',
                status_code=504,
                media_type="application/json",
            )
