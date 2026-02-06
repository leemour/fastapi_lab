"""Workflow and automation pipeline models."""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, Index
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


class Workflow(SQLModel, table=True):  # type: ignore[call-arg]
    """Define automation workflows with multiple steps."""

    __tablename__ = "workflows"

    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=255, unique=True, index=True)
    description: str | None = None
    enabled: bool = Field(default=True, index=True)
    trigger_type: str = Field(max_length=50, index=True)
    trigger_config: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    steps: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    variables: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    timeout_seconds: int = Field(default=300)
    retry_policy: dict[str, Any] = Field(
        default_factory=lambda: {"max_retries": 3, "backoff": "exponential"},
        sa_column=Column(JSON),
    )
    created_by: str | None = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (Index("idx_workflow_enabled_trigger", "enabled", "trigger_type"),)


class WorkflowExecution(SQLModel, table=True):  # type: ignore[call-arg]
    """Track workflow execution history."""

    __tablename__ = "workflow_executions"

    id: int | None = Field(default=None, primary_key=True, index=True)
    workflow_id: int = Field(index=True)
    status: str = Field(max_length=20, index=True)
    trigger_source: str | None = Field(default=None, max_length=100)
    trigger_data: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    started_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    completed_at: datetime | None = None
    duration_ms: int | None = None
    current_step: int = Field(default=0)
    total_steps: int = Field(default=0)
    step_results: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))
    variables: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    error_message: str | None = None
    error_traceback: str | None = None
    logs: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))

    __table_args__ = (
        Index("idx_workflow_exec_workflow_status", "workflow_id", "status"),
        Index("idx_workflow_exec_workflow_started", "workflow_id", "started_at"),
    )


# Request/Response Schemas
class WorkflowCreate(SQLModel):
    """Schema for creating a workflow."""

    name: str
    description: str | None = None
    enabled: bool = True
    trigger_type: str
    trigger_config: dict[str, Any] = Field(default_factory=dict)
    steps: list[dict[str, Any]] = Field(default_factory=list)
    variables: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = 300
    retry_policy: dict[str, Any] = Field(default_factory=lambda: {"max_retries": 3, "backoff": "exponential"})
    created_by: str | None = None


class WorkflowUpdate(SQLModel):
    """Schema for updating a workflow."""

    name: str | None = None
    description: str | None = None
    enabled: bool | None = None
    trigger_type: str | None = None
    trigger_config: dict[str, Any] | None = None
    steps: list[dict[str, Any]] | None = None
    variables: dict[str, Any] | None = None
    timeout_seconds: int | None = None
    retry_policy: dict[str, Any] | None = None


class WorkflowRead(SQLModel):
    """Schema for reading workflows."""

    id: int
    name: str
    description: str | None
    enabled: bool
    trigger_type: str
    trigger_config: dict[str, Any]
    steps: list[dict[str, Any]]
    variables: dict[str, Any]
    timeout_seconds: int
    retry_policy: dict[str, Any]
    created_by: str | None
    created_at: datetime
    updated_at: datetime


class WorkflowList(SQLModel):
    """Schema for paginated workflow list."""

    items: list[WorkflowRead]
    total: int
    page: int
    size: int
    pages: int


class WorkflowExecutionCreate(SQLModel):
    """Schema for creating a workflow execution."""

    workflow_id: int
    trigger_source: str | None = None
    trigger_data: dict[str, Any] | None = None


class WorkflowExecutionUpdate(SQLModel):
    """Schema for updating a workflow execution."""

    status: str | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = None
    current_step: int | None = None
    step_results: list[dict[str, Any]] | None = None
    variables: dict[str, Any] | None = None
    error_message: str | None = None
    error_traceback: str | None = None
    logs: list[dict[str, Any]] | None = None


class WorkflowExecutionRead(SQLModel):
    """Schema for reading workflow executions."""

    id: int
    workflow_id: int
    status: str
    trigger_source: str | None
    trigger_data: dict[str, Any] | None
    started_at: datetime
    completed_at: datetime | None
    duration_ms: int | None
    current_step: int
    total_steps: int
    step_results: list[dict[str, Any]]
    variables: dict[str, Any]
    error_message: str | None
    error_traceback: str | None
    logs: list[dict[str, Any]]


class WorkflowExecutionList(SQLModel):
    """Schema for paginated workflow execution list."""

    items: list[WorkflowExecutionRead]
    total: int
    page: int
    size: int
    pages: int
