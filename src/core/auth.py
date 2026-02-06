from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from src.core.config import settings
from src.core.logging import get_logger

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
logger = get_logger()


def require_api_key(api_key: str | None = Security(api_key_header)) -> None:
    if not api_key or api_key != settings.api_key:
        logger.warning("Invalid API key attempt", api_key_present=bool(api_key))
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
