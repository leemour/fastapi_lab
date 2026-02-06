"""Webhook inbox API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import desc, func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.logging import get_logger
from src.db import get_db
from src.models import (
    WebhookInbox,
    WebhookInboxCreate,
    WebhookInboxList,
    WebhookInboxRead,
    WebhookInboxUpdate,
)

logger = get_logger()
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/inbox/{source}", response_model=WebhookInboxRead, status_code=201)
async def receive_webhook(
    source: str,
    request: Request,
    event_type: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Receive and store a webhook from any source.

    This endpoint acts as a universal webhook receiver that captures all incoming requests.
    """
    # Extract request details
    headers = dict(request.headers)
    query_params = dict(request.query_params)

    # Try to parse body as JSON, fall back to raw text
    body = None
    raw_body = None
    try:
        body = await request.json()
    except Exception:
        raw_body = (await request.body()).decode("utf-8")

    # Create webhook entry
    webhook_data = WebhookInboxCreate(
        source=source,
        event_type=event_type,
        method=request.method,
        path=str(request.url.path),
        headers=headers,
        query_params=query_params,
        body=body,
        raw_body=raw_body,
        ip_address=request.client.host if request.client else None,
        user_agent=headers.get("user-agent"),
    )

    webhook = WebhookInbox(**webhook_data.model_dump())
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)

    logger.info("Webhook received", source=source, webhook_id=webhook.id, event_type=event_type)

    return webhook


@router.get("/inbox", response_model=WebhookInboxList)
async def list_webhooks(
    source: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    List webhook inbox entries with optional filtering.
    """
    query = select(WebhookInbox)

    if source:
        query = query.where(WebhookInbox.source == source)
    if status:
        query = query.where(WebhookInbox.status == status)

    query = query.order_by(desc(WebhookInbox.created_at))  # type: ignore[arg-type]

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    webhooks = result.scalars().all()

    return WebhookInboxList(
        items=webhooks,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/inbox/{webhook_id}", response_model=WebhookInboxRead)
async def get_webhook(
    webhook_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific webhook by ID.
    """
    result = await db.execute(select(WebhookInbox).where(WebhookInbox.id == webhook_id))
    webhook = result.scalar_one_or_none()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    return webhook


@router.patch("/inbox/{webhook_id}", response_model=WebhookInboxRead)
async def update_webhook(
    webhook_id: int,
    webhook_update: WebhookInboxUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a webhook inbox entry (e.g., mark as processed).
    """
    result = await db.execute(select(WebhookInbox).where(WebhookInbox.id == webhook_id))
    webhook = result.scalar_one_or_none()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Update fields
    for field, value in webhook_update.model_dump(exclude_unset=True).items():
        setattr(webhook, field, value)

    await db.commit()
    await db.refresh(webhook)

    logger.info("Webhook updated", webhook_id=webhook_id)

    return webhook


@router.delete("/inbox/{webhook_id}", status_code=204)
async def delete_webhook(
    webhook_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a webhook inbox entry.
    """
    result = await db.execute(select(WebhookInbox).where(WebhookInbox.id == webhook_id))
    webhook = result.scalar_one_or_none()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    await db.delete(webhook)
    await db.commit()

    logger.info("Webhook deleted", webhook_id=webhook_id)
