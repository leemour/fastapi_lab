#!/usr/bin/env python3
"""Example script showing how to use the automation models programmatically."""

import asyncio

from src.core.logging import get_logger, setup_logging
from src.db import get_db
from src.models import (
    ScheduledTask,
    ScheduledTaskCreate,
    WebhookInbox,
    WebhookInboxCreate,
    Workflow,
    WorkflowCreate,
    WorkflowExecution,
)

setup_logging()
logger = get_logger()


async def create_webhook_example():
    """Example: Create a webhook inbox entry."""
    logger.info("Creating webhook example...")

    async for db in get_db():
        webhook_data = WebhookInboxCreate(
            source="example",
            event_type="test",
            method="POST",
            path="/webhook/test",
            headers={"content-type": "application/json"},
            query_params={},
            body={"message": "Hello from example script"},
            ip_address="127.0.0.1",
        )

        webhook = WebhookInbox(**webhook_data.model_dump())
        db.add(webhook)
        await db.commit()
        await db.refresh(webhook)

        logger.info(f"Created webhook with ID: {webhook.id}")
        return webhook


async def create_task_example():
    """Example: Create a scheduled task."""
    logger.info("Creating task example...")

    async for db in get_db():
        task_data = ScheduledTaskCreate(
            name="Example Daily Task",
            description="This is an example task created programmatically",
            task_type="api_call",
            schedule="0 9 * * *",  # Daily at 9 AM
            enabled=True,
            config={
                "url": "https://httpbin.org/get",
                "method": "GET",
                "headers": {"User-Agent": "FastAPI-Lab"},
            },
            retry_policy={"max_retries": 3, "backoff": "exponential", "initial_delay": 60},
        )

        task = ScheduledTask(**task_data.model_dump())
        db.add(task)
        await db.commit()
        await db.refresh(task)

        logger.info(f"Created task with ID: {task.id}")
        return task


async def create_workflow_example():
    """Example: Create a workflow."""
    logger.info("Creating workflow example...")

    async for db in get_db():
        workflow_data = WorkflowCreate(
            name="Example User Onboarding Workflow",
            description="Multi-step workflow for onboarding new users",
            enabled=True,
            trigger_type="webhook",
            trigger_config={"event_type": "user.created"},
            steps=[
                {
                    "name": "Send Welcome Email",
                    "type": "email",
                    "config": {"template": "welcome", "to": "{{ user.email }}"},
                },
                {
                    "name": "Create User Account",
                    "type": "api_call",
                    "config": {
                        "url": "https://api.example.com/users",
                        "method": "POST",
                        "body": {"email": "{{ user.email }}", "name": "{{ user.name }}"},
                    },
                },
                {
                    "name": "Add to CRM",
                    "type": "api_call",
                    "config": {
                        "url": "https://crm.example.com/contacts",
                        "method": "POST",
                        "body": {"email": "{{ user.email }}"},
                    },
                },
                {
                    "name": "Send Slack Notification",
                    "type": "webhook",
                    "config": {
                        "url": "https://hooks.slack.com/services/XXX",
                        "body": {"text": "New user onboarded: {{ user.name }}"},
                    },
                },
            ],
            variables={"user": {"email": "", "name": ""}},
            timeout_seconds=300,
        )

        workflow = Workflow(**workflow_data.model_dump())
        db.add(workflow)
        await db.commit()
        await db.refresh(workflow)

        logger.info(f"Created workflow with ID: {workflow.id}")
        return workflow


async def trigger_workflow_example(workflow_id: int):
    """Example: Trigger a workflow execution."""
    logger.info(f"Triggering workflow {workflow_id}...")

    async for db in get_db():
        # Get the workflow first
        from sqlmodel import select

        result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
        workflow = result.scalar_one_or_none()

        if not workflow:
            logger.error(f"Workflow {workflow_id} not found")
            return None

        # Create execution
        execution = WorkflowExecution(
            workflow_id=workflow.id,
            status="pending",
            trigger_source="manual",
            trigger_data={"user": {"email": "john@example.com", "name": "John Doe"}},
            total_steps=len(workflow.steps),
            variables={
                **workflow.variables,
                "user": {"email": "john@example.com", "name": "John Doe"},
            },
        )

        db.add(execution)
        await db.commit()
        await db.refresh(execution)

        logger.info(f"Created workflow execution with ID: {execution.id}")
        return execution


async def main():
    """Main example function."""
    logger.info("Running automation examples...")

    try:
        # Example 1: Create a webhook
        webhook = await create_webhook_example()
        logger.info(f"Created webhook with ID: {webhook.id}")

        # Example 2: Create a task
        task = await create_task_example()
        logger.info(f"Created task with ID: {task.id}")

        # Example 3: Create a workflow
        workflow = await create_workflow_example()

        # Example 4: Trigger the workflow
        if workflow:
            execution = await trigger_workflow_example(workflow.id)
            logger.info(f"Created workflow execution with ID: {execution.id}")

        logger.info("✅ All examples completed successfully!")

    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
