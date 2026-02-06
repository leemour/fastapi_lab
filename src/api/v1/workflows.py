"""Workflow API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.logging import get_logger
from src.db import get_db
from src.models import (
    Workflow,
    WorkflowCreate,
    WorkflowExecution,
    WorkflowExecutionCreate,
    WorkflowExecutionList,
    WorkflowExecutionRead,
    WorkflowList,
    WorkflowRead,
    WorkflowUpdate,
)

logger = get_logger()
router = APIRouter(prefix="/workflows", tags=["workflows"])


# Workflows
@router.post("", response_model=WorkflowRead, status_code=201)
async def create_workflow(
    workflow: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new workflow.
    """
    # Check if workflow name already exists
    result = await db.execute(select(Workflow).where(Workflow.name == workflow.name))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Workflow with this name already exists")

    db_workflow = Workflow(**workflow.model_dump())
    db.add(db_workflow)
    await db.commit()
    await db.refresh(db_workflow)

    logger.info("Workflow created", workflow_id=db_workflow.id, name=db_workflow.name)

    return db_workflow


@router.get("", response_model=WorkflowList)
async def list_workflows(
    enabled: bool | None = None,
    trigger_type: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    List all workflows with optional filtering.
    """
    query = select(Workflow)

    if enabled is not None:
        query = query.where(Workflow.enabled == enabled)
    if trigger_type:
        query = query.where(Workflow.trigger_type == trigger_type)

    query = query.order_by(desc(Workflow.created_at))  # type: ignore[arg-type]

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    workflows = result.scalars().all()

    return WorkflowList(
        items=workflows,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/{workflow_id}", response_model=WorkflowRead)
async def get_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific workflow by ID.
    """
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return workflow


@router.patch("/{workflow_id}", response_model=WorkflowRead)
async def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a workflow.
    """
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Check name uniqueness if being updated
    if workflow_update.name and workflow_update.name != workflow.name:
        result = await db.execute(select(Workflow).where(Workflow.name == workflow_update.name))
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Workflow with this name already exists")

    # Update fields
    for field, value in workflow_update.model_dump(exclude_unset=True).items():
        setattr(workflow, field, value)

    await db.commit()
    await db.refresh(workflow)

    logger.info("Workflow updated", workflow_id=workflow_id)

    return workflow


@router.delete("/{workflow_id}", status_code=204)
async def delete_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a workflow.
    """
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    await db.delete(workflow)
    await db.commit()

    logger.info("Workflow deleted", workflow_id=workflow_id)


# Workflow Executions
@router.post("/{workflow_id}/executions", response_model=WorkflowExecutionRead, status_code=201)
async def create_execution(
    workflow_id: int,
    execution: WorkflowExecutionCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Start a new workflow execution.
    """
    # Verify workflow exists and is enabled
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if not workflow.enabled:
        raise HTTPException(status_code=400, detail="Workflow is disabled")

    # Create execution
    execution_data = execution.model_dump()
    execution_data["workflow_id"] = workflow_id
    execution_data["status"] = "pending"
    execution_data["total_steps"] = len(workflow.steps)
    execution_data["variables"] = {**workflow.variables, **(execution_data.get("trigger_data") or {})}

    db_execution = WorkflowExecution(**execution_data)
    db.add(db_execution)
    await db.commit()
    await db.refresh(db_execution)

    logger.info("Workflow execution created", execution_id=db_execution.id, workflow_id=workflow_id)

    return db_execution


@router.get("/{workflow_id}/executions", response_model=WorkflowExecutionList)
async def list_executions(
    workflow_id: int,
    status: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    List all executions for a specific workflow.
    """
    query = select(WorkflowExecution).where(WorkflowExecution.workflow_id == workflow_id)

    if status:
        query = query.where(WorkflowExecution.status == status)

    query = query.order_by(desc(WorkflowExecution.started_at))  # type: ignore[arg-type]

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    executions = result.scalars().all()

    return WorkflowExecutionList(
        items=executions,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/executions/{execution_id}", response_model=WorkflowExecutionRead)
async def get_execution(
    execution_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific workflow execution by ID.
    """
    result = await db.execute(select(WorkflowExecution).where(WorkflowExecution.id == execution_id))
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return execution
