from fastapi import APIRouter, Depends
from src.core.auth import require_api_key

router = APIRouter()


@router.get("/items", dependencies=[Depends(require_api_key)])
def get_items():
    return {"items": ["item1", "item2", "item3"]}
