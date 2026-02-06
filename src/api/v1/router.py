from fastapi import APIRouter

from src.api.v1 import api_logs, examples, health, items, tasks, webhooks, workflows

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(examples.router, tags=["examples"])

# Automation endpoints
api_router.include_router(webhooks.router)
api_router.include_router(tasks.router)
api_router.include_router(workflows.router)
api_router.include_router(api_logs.router)
