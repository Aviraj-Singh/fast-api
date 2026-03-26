from fastapi import APIRouter, Depends
from dependencies.database import get_db
from pydantic import BaseModel
from models.schemas import ItemCreate
from models.items import Item
from exceptions.items import ItemNotFoundException, ItemAlreadyExistsException

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

class PriceUpdate(BaseModel):
    price: int

@router.get("/")
def read_items(db = Depends(get_db)):
    return db.query(Item).all()

@router.post("/")
def create_items(item: ItemCreate, db = Depends(get_db)):
    existing_item = db.query(Item).filter(Item.name == item.name).first()
    if existing_item:
        raise ItemAlreadyExistsException(item.name)
    db_item = Item(
        name=item.name,
        price=item.price,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}")
def get_item(item_id: int, db = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        return item
    raise ItemNotFoundException(item_id)

@router.put("/{item_id}")
def update_price(item_id: int, discount: int, item: PriceUpdate, db = Depends(get_db)):
    final_price = item.price - (item.price * discount / 100)
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise ItemNotFoundException(item_id)
    item.price = final_price
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int, db = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted"}
    raise ItemNotFoundException(item_id)