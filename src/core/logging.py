import json
import sys
import traceback
from contextvars import ContextVar
from typing import Any

from loguru import logger

from src.core.config import settings

correlation_id_context: ContextVar[str | None] = ContextVar("correlation_id", default=None)
request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)


def serialize_record(record: dict) -> str:
    """Serialize log record to JSON format for production/staging."""
    correlation_id = correlation_id_context.get()
    request_id = request_id_context.get()

    subset = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "logger": record["name"],
        "message": record["message"],
        "correlation_id": correlation_id,
        "request_id": request_id,
    }

    if record.get("exception"):
        exc_info = record["exception"]
        subset["exception"] = {
            "type": exc_info.type.__name__,
            "value": str(exc_info.value),
            "traceback": "".join(
                traceback.format_exception(exc_info.type, exc_info.value, exc_info.traceback)
            ),
        }

    if record.get("extra"):
        subset["extra"] = record["extra"]

    return json.dumps(subset, default=str, ensure_ascii=False)


def format_record_dev(record: dict) -> str:
    """Format log record as colored key=value pairs for development."""
    correlation_id = correlation_id_context.get()
    request_id = request_id_context.get()

    parts = []
    parts.append(f"<green>{record['time'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}</green>")
    parts.append(f"<level>{record['level'].name:<8}</level>")
    parts.append(f"<level>{record['message']}</level>")

    if correlation_id:
        parts.append(f"<cyan>correlation_id={correlation_id}</cyan>")
    if request_id:
        parts.append(f"<cyan>request_id={request_id}</cyan>")

    parts.append(f"<blue>{record['name']}</blue>")

    if record.get("extra"):
        for key, value in record["extra"].items():
            # Skip internal context vars that are already displayed
            if key not in ("correlation_id", "request_id"):
                # Escape braces in value to prevent format string interpretation
                value_str = str(value).replace("{", "{{").replace("}", "}}")
                parts.append(f"<magenta>{key}</magenta>=<yellow>{value_str}</yellow>")

    result = " | ".join(parts) + "\n"

    # Exception will be handled by loguru's backtrace/diagnose settings
    return result


def setup_logging() -> None:
    """Configure Loguru based on the environment."""
    global logger
    logger.remove()

    environment = settings.environment.lower()

    if environment in ("production", "prod", "staging"):
        logger.add(
            sys.stdout,
            format="{extra[serialized]}",
            serialize=True,
            level="INFO",
            backtrace=True,
            diagnose=False,
        )
        logger = logger.patch(
            lambda record: record.update({"extra": {"serialized": serialize_record(record)}})
        )
    else:
        logger.add(
            sys.stdout,
            format=format_record_dev,
            level="DEBUG",
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

    logger.info(
        "Application started",
        environment=environment,
        app_name=settings.app_name,
    )


def bind_context_vars(correlation_id: str | None = None, request_id: str | None = None) -> None:
    """Bind correlation and request IDs to context variables."""
    if correlation_id:
        correlation_id_context.set(correlation_id)
    if request_id:
        request_id_context.set(request_id)


def clear_context_vars() -> None:
    """Clear context variables."""
    correlation_id_context.set(None)
    request_id_context.set(None)


def get_logger() -> Any:
    """Get configured logger instance."""
    return logger
