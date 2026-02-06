#!/usr/bin/env python3
"""Initialize database tables for the automation models."""

import asyncio

from src.core.logging import get_logger, setup_logging
from src.db import init_db

setup_logging()
logger = get_logger()


async def main():
    """Initialize all database tables."""
    logger.info("Starting database initialization...")

    try:
        await init_db()
        logger.info("✅ Database tables created successfully!")
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


if __name__ == "__main__":
    asyncio.run(main())
