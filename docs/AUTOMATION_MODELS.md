# Automation Models Documentation

This document describes the automation models added to the FastAPI Lab project for testing various automation workflows.

## Overview

The project now includes four main automation model groups:

1. **Webhook Inbox** - Universal webhook receiver and storage
2. **Scheduled Tasks** - Task scheduling and execution tracking
3. **Workflows** - Multi-step automation pipelines
4. **API Logs** - Request/response logging and monitoring

## Models

### 1. Webhook Inbox

**Purpose**: Capture and store incoming webhooks from any source for inspection, testing, and processing.

**Table**: `webhook_inbox`

**Use Cases**:
- Testing webhook integrations without external services
- Debugging webhook payloads
- Storing webhook history for audit trails
- Building webhook-triggered automations

**Key Fields**:
- `source`: Identifier for the webhook source (e.g., "github", "stripe")
- `event_type`: Type of event (e.g., "push", "payment_success")
- `status`: Processing status (received, processed, failed)
- `body`: Parsed JSON payload
- `raw_body`: Raw request body for non-JSON payloads

**Endpoints**:
```
POST   /v1/webhooks/inbox/{source}           # Receive webhook
GET    /v1/webhooks/inbox                    # List webhooks
GET    /v1/webhooks/inbox/{webhook_id}       # Get webhook details
PATCH  /v1/webhooks/inbox/{webhook_id}       # Update webhook status
DELETE /v1/webhooks/inbox/{webhook_id}       # Delete webhook
```

**Example Usage**:
```bash
# Receive a webhook from GitHub
curl -X POST http://localhost:8000/v1/webhooks/inbox/github?event_type=push \
  -H "Content-Type: application/json" \
  -d '{"ref": "refs/heads/main", "commits": [...]}'

# List all GitHub webhooks
curl http://localhost:8000/v1/webhooks/inbox?source=github
```

### 2. Scheduled Tasks

**Purpose**: Define recurring or scheduled tasks with execution tracking.

**Tables**:
- `scheduled_tasks` - Task definitions
- `task_executions` - Execution history

**Use Cases**:
- Cron-like scheduled jobs
- Recurring API calls
- Periodic data sync operations
- Scheduled report generation

**Key Fields (ScheduledTask)**:
- `task_type`: Type of task (webhook, cron, api_call)
- `schedule`: Cron expression or interval
- `enabled`: Whether the task is active
- `config`: Task-specific configuration
- `retry_policy`: Retry configuration on failures
- `success_count` / `failure_count`: Execution statistics

**Key Fields (TaskExecution)**:
- `status`: Execution status (pending, running, success, failed)
- `duration_ms`: Execution duration
- `input_data` / `output_data`: Execution data
- `error_message`: Error details if failed
- `logs`: Execution logs

**Endpoints**:
```
POST   /v1/tasks                              # Create task
GET    /v1/tasks                              # List tasks
GET    /v1/tasks/{task_id}                    # Get task details
PATCH  /v1/tasks/{task_id}                    # Update task
DELETE /v1/tasks/{task_id}                    # Delete task

POST   /v1/tasks/{task_id}/executions         # Create execution
GET    /v1/tasks/{task_id}/executions         # List executions
GET    /v1/tasks/executions/{execution_id}    # Get execution details
```

**Example Usage**:
```bash
# Create a scheduled task
curl -X POST http://localhost:8000/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Report",
    "task_type": "api_call",
    "schedule": "0 9 * * *",
    "enabled": true,
    "config": {
      "url": "https://api.example.com/report",
      "method": "GET"
    }
  }'

# List all enabled tasks
curl http://localhost:8000/v1/tasks?enabled=true
```

### 3. Workflows

**Purpose**: Define and execute multi-step automation workflows.

**Tables**:
- `workflows` - Workflow definitions
- `workflow_executions` - Execution history

**Use Cases**:
- Multi-step automation pipelines
- Event-driven workflows
- Complex business process automation
- Integration orchestration

**Key Fields (Workflow)**:
- `name`: Unique workflow name
- `trigger_type`: How workflow is triggered (webhook, schedule, manual, event)
- `trigger_config`: Trigger-specific configuration
- `steps`: Array of workflow steps
- `variables`: Default workflow variables
- `timeout_seconds`: Maximum execution time
- `retry_policy`: Retry configuration

**Key Fields (WorkflowExecution)**:
- `status`: Execution status (pending, running, success, failed, cancelled, timeout)
- `current_step` / `total_steps`: Progress tracking
- `step_results`: Results from each step
- `variables`: Runtime variables
- `logs`: Execution logs

**Endpoints**:
```
POST   /v1/workflows                          # Create workflow
GET    /v1/workflows                          # List workflows
GET    /v1/workflows/{workflow_id}            # Get workflow details
PATCH  /v1/workflows/{workflow_id}            # Update workflow
DELETE /v1/workflows/{workflow_id}            # Delete workflow

POST   /v1/workflows/{workflow_id}/executions # Start execution
GET    /v1/workflows/{workflow_id}/executions # List executions
GET    /v1/workflows/executions/{exec_id}     # Get execution details
```

**Example Usage**:
```bash
# Create a workflow
curl -X POST http://localhost:8000/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Order Processing",
    "trigger_type": "webhook",
    "enabled": true,
    "steps": [
      {"type": "validate", "config": {"schema": "order"}},
      {"type": "api_call", "config": {"url": "https://api.payment.com/charge"}},
      {"type": "email", "config": {"template": "order_confirmation"}}
    ],
    "timeout_seconds": 300
  }'

# Trigger a workflow execution
curl -X POST http://localhost:8000/v1/workflows/1/executions \
  -H "Content-Type: application/json" \
  -d '{
    "trigger_source": "manual",
    "trigger_data": {"order_id": "12345"}
  }'
```

### 4. API Logs

**Purpose**: Log and analyze API requests and responses.

**Table**: `api_logs`

**Use Cases**:
- API monitoring and debugging
- Performance analysis
- Audit trails
- Usage analytics

**Key Fields**:
- `correlation_id`: Request correlation ID
- `method` / `path`: Request details
- `status_code`: Response status
- `request_headers` / `request_body`: Request data
- `response_headers` / `response_body`: Response data
- `duration_ms`: Request duration
- `user_id`: User identifier (if authenticated)

**Endpoints**:
```
GET    /v1/api-logs                           # List API logs
GET    /v1/api-logs/{log_id}                  # Get log details
GET    /v1/api-logs/stats/summary             # Get statistics
DELETE /v1/api-logs/{log_id}                  # Delete log
```

**Example Usage**:
```bash
# List recent API logs
curl http://localhost:8000/v1/api-logs?page=1&size=50

# Get statistics for the last 24 hours
curl http://localhost:8000/v1/api-logs/stats/summary

# Filter logs by path and status
curl "http://localhost:8000/v1/api-logs?path=/v1/webhooks&status_code=200"
```

## Database Setup

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Ensure PostgreSQL is running:
```bash
docker-compose up -d postgres
```

3. Initialize database tables:
```bash
python scripts/init_tables.py
```

Or the tables will be automatically created on application startup.

### Technology Stack

- **SQLModel**: Combines SQLAlchemy ORM with Pydantic validation
- **asyncpg**: Async PostgreSQL driver
- **PostgreSQL**: Primary database

### Database URL

Configure in `.env`:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5433/fastapi_lab
```

## Testing the Models

### Using the API

Start the application:
```bash
# With Docker
docker-compose up

# Or locally
uvicorn main:app --reload
```

Access the interactive API docs at: http://localhost:8000/docs

### Example Test Flow

1. **Create a webhook inbox entry**:
   - POST to `/v1/webhooks/inbox/test`
   - Check it appears in GET `/v1/webhooks/inbox`

2. **Create a scheduled task**:
   - POST to `/v1/tasks` with task definition
   - Create an execution: POST to `/v1/tasks/{id}/executions`
   - View execution history

3. **Create and execute a workflow**:
   - POST to `/v1/workflows` with workflow definition
   - Trigger execution: POST to `/v1/workflows/{id}/executions`
   - Monitor progress via GET requests

4. **View API logs**:
   - All API requests are logged (if logging middleware is enabled)
   - View stats: GET `/v1/api-logs/stats/summary`

## Architecture Notes

### SQLModel Benefits

- **Single Source of Truth**: Model and schema in one class
- **Type Safety**: Full Python type hints
- **Validation**: Built-in Pydantic validation
- **Less Boilerplate**: No need for separate ORM models and Pydantic schemas

### Index Strategy

All tables include strategic indexes for:
- Primary keys (automatic)
- Foreign key relationships (task_id, workflow_id)
- Common query patterns (status + created_at)
- Filter fields (enabled, source, event_type)

### JSON Fields

JSON columns are used for flexible data storage:
- `config`, `variables`, `trigger_config`: Configuration objects
- `body`, `headers`, `query_params`: Request data
- `step_results`, `logs`: Execution data

This allows for flexible schemas without frequent migrations.

## Future Enhancements

Potential improvements:
- [ ] Add real task scheduler (APScheduler, Celery)
- [ ] Implement workflow step execution engine
- [ ] Add webhook signature verification
- [ ] Implement rate limiting per source
- [ ] Add data retention policies
- [ ] Add export functionality (CSV, JSON)
- [ ] Add real-time execution monitoring (WebSockets)
- [ ] Add workflow visual builder
- [ ] Implement step retry logic
- [ ] Add notification system (email, Slack, webhooks)
