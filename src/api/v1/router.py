from fastapi import APIRouter
from src.api.v1 import examples, health, items

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(examples.router, tags=["examples"])
