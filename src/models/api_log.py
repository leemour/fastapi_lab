"""API request/response logging models for auditing and monitoring."""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, Index
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


class APILog(SQLModel, table=True):  # type: ignore[call-arg]
    """Log API requests and responses for monitoring and debugging."""

    __tablename__ = "api_logs"

    id: int | None = Field(default=None, primary_key=True, index=True)
    correlation_id: str | None = Field(default=None, max_length=36, index=True)
    method: str = Field(max_length=10, index=True)
    path: str = Field(max_length=500, index=True)
    full_url: str | None = Field(default=None, max_length=1000)
    status_code: int = Field(index=True)
    request_headers: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    request_body: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    response_headers: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    response_body: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    duration_ms: int
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=500)
    user_id: str | None = Field(default=None, max_length=100, index=True)
    error_message: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    __table_args__ = (
        Index("idx_api_log_path_created", "path", "created_at"),
        Index("idx_api_log_status_created", "status_code", "created_at"),
        Index("idx_api_log_user_created", "user_id", "created_at"),
    )


class APILogCreate(SQLModel):
    """Schema for creating an API log entry."""

    correlation_id: str | None = None
    method: str
    path: str
    full_url: str | None = None
    status_code: int
    request_headers: dict[str, Any] = Field(default_factory=dict)
    request_body: dict[str, Any] | None = None
    response_headers: dict[str, Any] = Field(default_factory=dict)
    response_body: dict[str, Any] | None = None
    duration_ms: int
    ip_address: str | None = None
    user_agent: str | None = None
    user_id: str | None = None
    error_message: str | None = None


class APILogRead(SQLModel):
    """Schema for reading API logs."""

    id: int
    correlation_id: str | None
    method: str
    path: str
    full_url: str | None
    status_code: int
    request_headers: dict[str, Any]
    request_body: dict[str, Any] | None
    response_headers: dict[str, Any]
    response_body: dict[str, Any] | None
    duration_ms: int
    ip_address: str | None
    user_agent: str | None
    user_id: str | None
    error_message: str | None
    created_at: datetime


class APILogList(SQLModel):
    """Schema for paginated API log list."""

    items: list[APILogRead]
    total: int
    page: int
    size: int
    pages: int


class APILogStats(SQLModel):
    """Schema for API log statistics."""

    total_requests: int
    success_rate: float
    average_duration_ms: float
    requests_by_status: dict[int, int]
    requests_by_path: dict[str, int]
    requests_by_method: dict[str, int]
