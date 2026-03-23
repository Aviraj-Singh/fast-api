from fastapi import APIRouter, Depends
from dependencies.db import get_items_db
from pydantic import BaseModel
from exceptions.items import ItemNotFoundException

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

class PriceUpdate(BaseModel):
    price: int

@router.get("/")
def read_items(db = Depends(get_items_db)):
    return db

@router.get("/items/{item_id}")
def get_item(item_id: int, db = Depends(get_items_db)):
    if item_id not in db:
        raise ItemNotFoundException(item_id)
    return db[item_id]

@router.put("/{item_id}")
def update_price(item_id: int, discount: int, item: PriceUpdate):
    final_price = item.price - (item.price * discount / 100)

    return {
        "item_id": item_id,
        "final_price": final_price
    }