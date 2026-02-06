"""Scheduled tasks API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.logging import get_logger
from src.db import get_db
from src.models import (
    ScheduledTask,
    ScheduledTaskCreate,
    ScheduledTaskList,
    ScheduledTaskRead,
    ScheduledTaskUpdate,
    TaskExecution,
    TaskExecutionCreate,
    TaskExecutionList,
    TaskExecutionRead,
)

logger = get_logger()
router = APIRouter(prefix="/tasks", tags=["tasks"])


# Scheduled Tasks
@router.post("", response_model=ScheduledTaskRead, status_code=201)
async def create_task(
    task: ScheduledTaskCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new scheduled task.
    """
    db_task = ScheduledTask(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    logger.info("Scheduled task created", task_id=db_task.id, name=db_task.name)

    return db_task


@router.get("", response_model=ScheduledTaskList)
async def list_tasks(
    enabled: bool | None = None,
    task_type: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    List all scheduled tasks with optional filtering.
    """
    query = select(ScheduledTask)

    if enabled is not None:
        query = query.where(ScheduledTask.enabled == enabled)
    if task_type:
        query = query.where(ScheduledTask.task_type == task_type)

    query = query.order_by(desc(ScheduledTask.created_at))  # type: ignore[arg-type]

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    tasks = result.scalars().all()

    return ScheduledTaskList(
        items=tasks,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/{task_id}", response_model=ScheduledTaskRead)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific scheduled task by ID.
    """
    result = await db.execute(select(ScheduledTask).where(ScheduledTask.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/{task_id}", response_model=ScheduledTaskRead)
async def update_task(
    task_id: int,
    task_update: ScheduledTaskUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a scheduled task.
    """
    result = await db.execute(select(ScheduledTask).where(ScheduledTask.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    logger.info("Scheduled task updated", task_id=task_id)

    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a scheduled task.
    """
    result = await db.execute(select(ScheduledTask).where(ScheduledTask.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()

    logger.info("Scheduled task deleted", task_id=task_id)


# Task Executions
@router.post("/{task_id}/executions", response_model=TaskExecutionRead, status_code=201)
async def create_execution(
    task_id: int,
    execution: TaskExecutionCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new task execution record.
    """
    # Verify task exists
    result = await db.execute(select(ScheduledTask).where(ScheduledTask.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Ensure task_id matches
    execution_data = execution.model_dump()
    execution_data["task_id"] = task_id

    db_execution = TaskExecution(**execution_data)
    db.add(db_execution)
    await db.commit()
    await db.refresh(db_execution)

    logger.info("Task execution created", execution_id=db_execution.id, task_id=task_id)

    return db_execution


@router.get("/{task_id}/executions", response_model=TaskExecutionList)
async def list_executions(
    task_id: int,
    status: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    List all executions for a specific task.
    """
    query = select(TaskExecution).where(TaskExecution.task_id == task_id)

    if status:
        query = query.where(TaskExecution.status == status)

    query = query.order_by(desc(TaskExecution.started_at))  # type: ignore[arg-type]

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    executions = result.scalars().all()

    return TaskExecutionList(
        items=executions,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/executions/{execution_id}", response_model=TaskExecutionRead)
async def get_execution(
    execution_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific task execution by ID.
    """
    result = await db.execute(select(TaskExecution).where(TaskExecution.id == execution_id))
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return execution
