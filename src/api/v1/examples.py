from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from src.core.logging import get_logger

router = APIRouter(prefix="/examples", tags=["examples"])
logger = get_logger()


class ExampleData(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    value: int = Field(..., ge=0, le=1000)
    metadata: dict | None = None


@router.get("/test-logging")
async def test_logging(request: Request):
    """Test various log levels."""
    logger.debug("This is a debug message", endpoint="test-logging")
    logger.info("This is an info message", endpoint="test-logging")
    logger.warning("This is a warning message", endpoint="test-logging")
    logger.error("This is an error message (not an exception)", endpoint="test-logging")

    return {
        "message": "Logged messages at various levels",
        "correlation_id": request.state.correlation_id,
        "request_id": request.state.request_id,
    }


@router.post("/process-data")
async def process_data(data: ExampleData, request: Request):
    """Process data with contextual logging."""
    logger.info(
        "Processing data",
        data_name=data.name,
        data_value=data.value,
        has_metadata=data.metadata is not None,
    )

    if data.value > 900:
        logger.warning(
            "High value detected",
            value=data.value,
            threshold=900,
        )

    if data.metadata:
        logger.debug(
            "Processing metadata",
            metadata_keys=list(data.metadata.keys()),
            metadata_size=len(data.metadata),
        )

    result = {
        "processed": True,
        "original_value": data.value,
        "doubled_value": data.value * 2,
        "correlation_id": request.state.correlation_id,
        "request_id": request.state.request_id,
    }

    logger.info("Data processing completed", result=result)
    return result


@router.get("/trigger-http-error/{error_code}")
async def trigger_http_error(error_code: int):
    """Trigger an HTTP error for testing error logging."""
    logger.info(f"Triggering HTTP error {error_code}")

    if error_code == 400:
        raise HTTPException(status_code=400, detail="Bad request example")
    elif error_code == 404:
        raise HTTPException(status_code=404, detail="Resource not found example")
    elif error_code == 500:
        raise HTTPException(status_code=500, detail="Internal server error example")
    else:
        return {"message": f"No error triggered for code {error_code}"}


@router.get("/trigger-exception")
async def trigger_exception():
    """Trigger an unhandled exception for testing exception logging."""
    logger.info("About to trigger an exception")

    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.exception("Division by zero occurred")
        raise

    return {"result": result}


@router.get("/simulate-slow-operation")
async def simulate_slow_operation(delay_ms: int = 100):
    """Simulate a slow operation to test request timing logs."""
    import asyncio

    logger.info(f"Starting slow operation with {delay_ms}ms delay")

    await asyncio.sleep(delay_ms / 1000)

    logger.info(f"Slow operation completed after {delay_ms}ms")
    return {"delayed_ms": delay_ms, "status": "completed"}


@router.post("/validate-input")
async def validate_input(data: ExampleData):
    """Test validation error logging with invalid input."""
    logger.info("Validating input data", data=data.model_dump())

    if "forbidden" in data.name.lower():
        logger.error("Forbidden word detected in name", name=data.name)
        raise HTTPException(status_code=403, detail="Forbidden word in name")

    return {"validated": True, "data": data.model_dump()}