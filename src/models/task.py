"""Task and job models for automation workflows."""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, Index
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


class ScheduledTask(SQLModel, table=True):  # type: ignore[call-arg]
    """Scheduled tasks for automation workflows."""

    __tablename__ = "scheduled_tasks"

    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=255, index=True)
    description: str | None = None
    task_type: str = Field(max_length=50, index=True)
    schedule: str | None = Field(default=None, max_length=100)
    enabled: bool = Field(default=True, index=True)
    config: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    retry_policy: dict[str, Any] = Field(
        default_factory=lambda: {"max_retries": 3, "backoff": "exponential", "initial_delay": 60},
        sa_column=Column(JSON),
    )
    last_run_at: datetime | None = None
    next_run_at: datetime | None = Field(default=None, index=True)
    success_count: int = Field(default=0)
    failure_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (
        Index("idx_task_enabled_next_run", "enabled", "next_run_at"),
        Index("idx_task_type_enabled", "task_type", "enabled"),
    )


class TaskExecution(SQLModel, table=True):  # type: ignore[call-arg]
    """Track individual task execution history."""

    __tablename__ = "task_executions"

    id: int | None = Field(default=None, primary_key=True, index=True)
    task_id: int = Field(index=True)
    status: str = Field(max_length=20, index=True)
    started_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    completed_at: datetime | None = None
    duration_ms: int | None = None
    input_data: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    output_data: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    error_message: str | None = None
    error_traceback: str | None = None
    retry_count: int = Field(default=0)
    logs: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))

    __table_args__ = (
        Index("idx_execution_task_status", "task_id", "status"),
        Index("idx_execution_task_started", "task_id", "started_at"),
    )


# Request/Response Schemas
class ScheduledTaskCreate(SQLModel):
    """Schema for creating a scheduled task."""

    name: str
    description: str | None = None
    task_type: str
    schedule: str | None = None
    enabled: bool = True
    config: dict[str, Any] = Field(default_factory=dict)
    retry_policy: dict[str, Any] = Field(
        default_factory=lambda: {"max_retries": 3, "backoff": "exponential", "initial_delay": 60}
    )


class ScheduledTaskUpdate(SQLModel):
    """Schema for updating a scheduled task."""

    name: str | None = None
    description: str | None = None
    task_type: str | None = None
    schedule: str | None = None
    enabled: bool | None = None
    config: dict[str, Any] | None = None
    retry_policy: dict[str, Any] | None = None


class ScheduledTaskRead(SQLModel):
    """Schema for reading scheduled tasks."""

    id: int
    name: str
    description: str | None
    task_type: str
    schedule: str | None
    enabled: bool
    config: dict[str, Any]
    retry_policy: dict[str, Any]
    last_run_at: datetime | None
    next_run_at: datetime | None
    success_count: int
    failure_count: int
    created_at: datetime
    updated_at: datetime


class ScheduledTaskList(SQLModel):
    """Schema for paginated scheduled task list."""

    items: list[ScheduledTaskRead]
    total: int
    page: int
    size: int
    pages: int


class TaskExecutionCreate(SQLModel):
    """Schema for creating a task execution."""

    task_id: int
    status: str
    input_data: dict[str, Any] | None = None


class TaskExecutionUpdate(SQLModel):
    """Schema for updating a task execution."""

    status: str | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = None
    output_data: dict[str, Any] | None = None
    error_message: str | None = None
    error_traceback: str | None = None
    retry_count: int | None = None
    logs: list[dict[str, Any]] | None = None


class TaskExecutionRead(SQLModel):
    """Schema for reading task executions."""

    id: int
    task_id: int
    status: str
    started_at: datetime
    completed_at: datetime | None
    duration_ms: int | None
    input_data: dict[str, Any] | None
    output_data: dict[str, Any] | None
    error_message: str | None
    error_traceback: str | None
    retry_count: int
    logs: list[dict[str, Any]]


class TaskExecutionList(SQLModel):
    """Schema for paginated task execution list."""

    items: list[TaskExecutionRead]
    total: int
    page: int
    size: int
    pages: int
