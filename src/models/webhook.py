"""Webhook inbox models for receiving and storing webhook payloads."""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, Index
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


class WebhookInbox(SQLModel, table=True):  # type: ignore[call-arg]
    """Store incoming webhook requests for inspection and testing."""

    __tablename__ = "webhook_inbox"

    id: int | None = Field(default=None, primary_key=True, index=True)
    source: str = Field(max_length=255, index=True)
    event_type: str | None = Field(default=None, max_length=100, index=True)
    method: str = Field(max_length=10)
    path: str = Field(max_length=500)
    headers: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    query_params: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    body: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    raw_body: str | None = Field(default=None)
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=500)
    status: str = Field(default="received", max_length=20, index=True)
    processed_at: datetime | None = Field(default=None)
    error_message: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    __table_args__ = (
        Index("idx_webhook_source_created", "source", "created_at"),
        Index("idx_webhook_status_created", "status", "created_at"),
    )


class WebhookInboxCreate(SQLModel):
    """Schema for creating a webhook inbox entry."""

    source: str = Field(max_length=255)
    event_type: str | None = None
    method: str = Field(max_length=10)
    path: str = Field(max_length=500)
    headers: dict[str, Any] = Field(default_factory=dict)
    query_params: dict[str, Any] = Field(default_factory=dict)
    body: dict[str, Any] | None = None
    raw_body: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None


class WebhookInboxUpdate(SQLModel):
    """Schema for updating a webhook inbox entry."""

    status: str | None = None
    processed_at: datetime | None = None
    error_message: str | None = None


class WebhookInboxRead(SQLModel):
    """Schema for reading webhook inbox entries."""

    id: int
    source: str
    event_type: str | None
    method: str
    path: str
    headers: dict[str, Any]
    query_params: dict[str, Any]
    body: dict[str, Any] | None
    raw_body: str | None
    ip_address: str | None
    user_agent: str | None
    status: str
    processed_at: datetime | None
    error_message: str | None
    created_at: datetime


class WebhookInboxList(SQLModel):
    """Schema for paginated webhook inbox list."""

    items: list[WebhookInboxRead]
    total: int
    page: int
    size: int
    pages: int
