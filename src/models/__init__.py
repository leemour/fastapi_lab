"""Database models for automation tasks."""

from src.models.api_log import APILog, APILogCreate, APILogList, APILogRead, APILogStats
from src.models.task import (
    ScheduledTask,
    ScheduledTaskCreate,
    ScheduledTaskList,
    ScheduledTaskRead,
    ScheduledTaskUpdate,
    TaskExecution,
    TaskExecutionCreate,
    TaskExecutionList,
    TaskExecutionRead,
    TaskExecutionUpdate,
)
from src.models.webhook import (
    WebhookInbox,
    WebhookInboxCreate,
    WebhookInboxList,
    WebhookInboxRead,
    WebhookInboxUpdate,
)
from src.models.workflow import (
    Workflow,
    WorkflowCreate,
    WorkflowExecution,
    WorkflowExecutionCreate,
    WorkflowExecutionList,
    WorkflowExecutionRead,
    WorkflowExecutionUpdate,
    WorkflowList,
    WorkflowRead,
    WorkflowUpdate,
)

__all__ = [
    # Webhook models
    "WebhookInbox",
    "WebhookInboxCreate",
    "WebhookInboxUpdate",
    "WebhookInboxRead",
    "WebhookInboxList",
    # Task models
    "ScheduledTask",
    "ScheduledTaskCreate",
    "ScheduledTaskUpdate",
    "ScheduledTaskRead",
    "ScheduledTaskList",
    "TaskExecution",
    "TaskExecutionCreate",
    "TaskExecutionUpdate",
    "TaskExecutionRead",
    "TaskExecutionList",
    # API Log models
    "APILog",
    "APILogCreate",
    "APILogRead",
    "APILogList",
    "APILogStats",
    # Workflow models
    "Workflow",
    "WorkflowCreate",
    "WorkflowUpdate",
    "WorkflowRead",
    "WorkflowList",
    "WorkflowExecution",
    "WorkflowExecutionCreate",
    "WorkflowExecutionUpdate",
    "WorkflowExecutionRead",
    "WorkflowExecutionList",
]
