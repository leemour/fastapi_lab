import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.logging import get_logger

logger = get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request and response data."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()

        # Detailed log at the beginning
        request_data = {
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params) if request.query_params else None,
            "path_params": request.path_params if hasattr(request, "path_params") else None,
            "client": f"{request.client.host}:{request.client.port}" if request.client else None,
            "user_agent": request.headers.get("User-Agent"),
            "content_type": request.headers.get("Content-Type"),
            "correlation_id": getattr(request.state, "correlation_id", None),
            "request_id": getattr(request.state, "request_id", None),
        }

        important_headers = {
            "Authorization": request.headers.get("Authorization") is not None,
            "X-API-Key": request.headers.get("X-API-Key") is not None,
            "Accept": request.headers.get("Accept"),
            "Accept-Language": request.headers.get("Accept-Language"),
        }
        request_data["headers_info"] = important_headers

        logger.info(
            "👉 Request started",
            **request_data
        )

        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time

            # Minimal log at the end (just status and timing)
            logger.info(
                f"🏁 {response.status_code} Request completed",
                status_code=response.status_code,
                process_time_ms=round(process_time * 1000, 2),
            )

            response.headers["X-Process-Time"] = str(process_time)
            return response

        except Exception as e:
            process_time = time.perf_counter() - start_time
            logger.exception(
                "Request failed with exception",
                method=request.method,
                path=request.url.path,
                process_time_ms=round(process_time * 1000, 2),
                correlation_id=getattr(request.state, "correlation_id", None),
                request_id=getattr(request.state, "request_id", None),
                exception_type=type(e).__name__,
            )
            raise
