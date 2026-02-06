import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.logging import bind_context_vars, clear_context_vars


class CorrelationMiddleware(BaseHTTPMiddleware):
    """Middleware to handle correlation and request IDs for request tracking."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = request.headers.get("X-Request-ID")
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        bind_context_vars(correlation_id=correlation_id, request_id=request_id)

        request.state.correlation_id = correlation_id
        request.state.request_id = request_id

        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            clear_context_vars()