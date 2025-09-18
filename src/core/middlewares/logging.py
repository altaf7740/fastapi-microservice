import time
from typing import Awaitable, Callable
from uuid import uuid4

from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIDAndLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        request_id = str(uuid4())
        log = logger.bind(request_id=request_id)
        request.state.request_id = request_id
        log.info(
            f"Incoming request: {request.method} {request.url} from {request.client.host if request.client else 'unknown'}"
        )
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            log.exception(f"Unhandled error: {str(e)}")
            return JSONResponse({"detail": "Internal Server Error", "request_id": request_id}, status_code=500)
        process_time = round((time.time() - start_time) * 1000, 2)
        log.info(f"Completed in {process_time}ms with status {response.status_code}")
        response.headers["X-Request-ID"] = request_id
        return response
