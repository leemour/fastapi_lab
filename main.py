from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.core.config import settings
from src.api.v1.router import api_router


app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(api_router, prefix="/v1")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
