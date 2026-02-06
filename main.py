from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from src.api.v1.router import api_router
from src.core.config import settings
from src.core.exception_handlers import (
    general_exception_handler,
    http_exception_handler,
    starlette_exception_handler,
    validation_exception_handler,
)
from src.core.logging import get_logger, setup_logging
from src.db import init_db
from src.middleware.correlation import CorrelationMiddleware
from src.middleware.request_logging import RequestLoggingMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

setup_logging()
logger = get_logger()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Initializing database")
    await init_db()
    logger.info("Database initialized successfully")


app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CorrelationMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, starlette_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(api_router, prefix="/v1")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    logger.info("Reading item", item_id=item_id, query=q)
    if item_id < 1:
        logger.warning("Invalid item ID requested", item_id=item_id)
        raise HTTPException(status_code=400, detail="Invalid item ID")
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    logger.info("Creating new item", item_name=item.name, price=item.price)
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
        logger.debug("Calculated price with tax", price_with_tax=price_with_tax)
    return item_dict


if __name__ == "__main__":
    import uvicorn

    # Configure uvicorn to use our logging
    log_config = uvicorn.config.LOGGING_CONFIG
    # Disable default access logs since we have our own middleware logging
    log_config["loggers"]["uvicorn.access"]["handlers"] = []
    log_config["loggers"]["uvicorn.access"]["propagate"] = False

    uvicorn.run(
        app,
        host="0.0.0.0",  # nosec B104 - Binding to all interfaces is intentional for Docker
        port=8000,
        log_config=log_config,
        access_log=False,  # Disable access logs completely
    )
