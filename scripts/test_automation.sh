#!/bin/bash
# Test automation endpoints

BASE_URL="http://localhost:8000/v1"

echo "🧪 Testing Automation Endpoints"
echo "================================"
echo ""

# Test 1: Webhook Inbox
echo "1️⃣  Testing Webhook Inbox..."
WEBHOOK_RESPONSE=$(curl -s -X POST "$BASE_URL/webhooks/inbox/test" \
  -H "Content-Type: application/json" \
  -d '{"event": "test", "data": {"message": "Hello from webhook test"}}')

WEBHOOK_ID=$(echo $WEBHOOK_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$WEBHOOK_ID" ]; then
  echo "✅ Webhook created with ID: $WEBHOOK_ID"
else
  echo "❌ Failed to create webhook"
fi
echo ""

# Test 2: Scheduled Task
echo "2️⃣  Testing Scheduled Tasks..."
TASK_RESPONSE=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Task",
    "task_type": "api_call",
    "schedule": "0 * * * *",
    "enabled": true,
    "config": {"url": "https://httpbin.org/get"}
  }')

TASK_ID=$(echo $TASK_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$TASK_ID" ]; then
  echo "✅ Task created with ID: $TASK_ID"

  # Create an execution
  EXEC_RESPONSE=$(curl -s -X POST "$BASE_URL/tasks/$TASK_ID/executions" \
    -H "Content-Type: application/json" \
    -d "{\"task_id\": $TASK_ID, \"status\": \"success\", \"input_data\": {}}")

  EXEC_ID=$(echo $EXEC_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

  if [ -n "$EXEC_ID" ]; then
    echo "✅ Execution created with ID: $EXEC_ID"
  fi
else
  echo "❌ Failed to create task"
fi
echo ""

# Test 3: Workflow
echo "3️⃣  Testing Workflows..."
WORKFLOW_RESPONSE=$(curl -s -X POST "$BASE_URL/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Workflow",
    "trigger_type": "manual",
    "enabled": true,
    "steps": [
      {"type": "log", "config": {"message": "Step 1"}},
      {"type": "log", "config": {"message": "Step 2"}}
    ]
  }')

WORKFLOW_ID=$(echo $WORKFLOW_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$WORKFLOW_ID" ]; then
  echo "✅ Workflow created with ID: $WORKFLOW_ID"

  # Start an execution
  WF_EXEC_RESPONSE=$(curl -s -X POST "$BASE_URL/workflows/$WORKFLOW_ID/executions" \
    -H "Content-Type: application/json" \
    -d "{\"workflow_id\": $WORKFLOW_ID, \"trigger_source\": \"test\"}")

  WF_EXEC_ID=$(echo $WF_EXEC_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

  if [ -n "$WF_EXEC_ID" ]; then
    echo "✅ Workflow execution created with ID: $WF_EXEC_ID"
  fi
else
  echo "❌ Failed to create workflow"
fi
echo ""

# Summary
echo "📊 Summary"
echo "=========="
echo "View all webhooks:  curl $BASE_URL/webhooks/inbox"
echo "View all tasks:     curl $BASE_URL/tasks"
echo "View all workflows: curl $BASE_URL/workflows"
echo ""
echo "Or visit the interactive docs: http://localhost:8000/docs"
