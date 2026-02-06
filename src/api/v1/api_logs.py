"""API logs endpoints."""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.logging import get_logger
from src.db import get_db
from src.models import APILog, APILogList, APILogRead, APILogStats

logger = get_logger()
router = APIRouter(prefix="/api-logs", tags=["api-logs"])


@router.get("", response_model=APILogList)
async def list_api_logs(
    path: str | None = None,
    method: str | None = None,
    status_code: int | None = None,
    user_id: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    List API logs with optional filtering.
    """
    query = select(APILog)

    if path:
        query = query.where(APILog.path.like(f"%{path}%"))  # type: ignore[attr-defined]
    if method:
        query = query.where(APILog.method == method.upper())
    if status_code:
        query = query.where(APILog.status_code == status_code)
    if user_id:
        query = query.where(APILog.user_id == user_id)
    if start_date:
        query = query.where(APILog.created_at >= start_date)
    if end_date:
        query = query.where(APILog.created_at <= end_date)

    query = query.order_by(desc(APILog.created_at))  # type: ignore[arg-type]

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    logs = result.scalars().all()

    return APILogList(
        items=logs,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/{log_id}", response_model=APILogRead)
async def get_api_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific API log by ID.
    """
    result = await db.execute(select(APILog).where(APILog.id == log_id))
    log = result.scalar_one_or_none()

    if not log:
        raise HTTPException(status_code=404, detail="API log not found")

    return log


@router.get("/stats/summary", response_model=APILogStats)
async def get_api_stats(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get API statistics for a given time period.
    """
    # Default to last 24 hours if no dates provided
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=1)

    query = select(APILog).where(
        APILog.created_at >= start_date,
        APILog.created_at <= end_date,
    )

    result = await db.execute(query)
    logs = result.scalars().all()

    if not logs:
        return APILogStats(
            total_requests=0,
            success_rate=0.0,
            average_duration_ms=0.0,
            requests_by_status={},
            requests_by_path={},
            requests_by_method={},
        )

    # Calculate statistics
    total_requests = len(logs)
    successful_requests = sum(1 for log in logs if 200 <= log.status_code < 400)
    success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0.0
    average_duration = sum(log.duration_ms for log in logs) / total_requests if total_requests > 0 else 0.0

    # Group by status code
    requests_by_status: dict[int, int] = {}
    for log in logs:
        requests_by_status[log.status_code] = requests_by_status.get(log.status_code, 0) + 1

    # Group by path
    requests_by_path: dict[str, int] = {}
    for log in logs:
        requests_by_path[log.path] = requests_by_path.get(log.path, 0) + 1

    # Group by method
    requests_by_method: dict[str, int] = {}
    for log in logs:
        requests_by_method[log.method] = requests_by_method.get(log.method, 0) + 1

    return APILogStats(
        total_requests=total_requests,
        success_rate=round(success_rate, 2),
        average_duration_ms=round(average_duration, 2),
        requests_by_status=requests_by_status,
        requests_by_path=requests_by_path,
        requests_by_method=requests_by_method,
    )


@router.delete("/{log_id}", status_code=204)
async def delete_api_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete an API log entry.
    """
    result = await db.execute(select(APILog).where(APILog.id == log_id))
    log = result.scalar_one_or_none()

    if not log:
        raise HTTPException(status_code=404, detail="API log not found")

    await db.delete(log)
    await db.commit()

    logger.info("API log deleted", log_id=log_id)
