"""
Day 1 - FastAPI Learning
Topics covered:
- Request lifecycle
- REST APIs
- CRUD operations
- Validation (Pydantic)
- Status codes
"""

from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

items = {
    1: {"name": "iPhone", "price": 100000}
}

class ItemCreate(BaseModel):
    name: str
    price: int

    # for allowing extra unknown fields
    class Config:
       extra = "allow"

class ItemResponse(BaseModel):
    name: str
    price: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None

class Item(BaseModel):
    name: str
    price: int

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"message": "This is my first FastAPI app"}

#path parameters: Dynamic values inside URL
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"product_id": product_id}

@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {
        "user_id": user_id,
        "order_id": order_id
    }

@app.get("/students/{student_id}/courses/{course_id}")
def get_course(student_id: int, course_id: int):
    return {"student_id": student_id, "course_id": course_id}

@app.get("/items")
# if we miss price in param, it will throw 422 as both are required param
# def get_items(name: str, price: int):
def get_items(name: str, price: Optional[int] = None):
    return {"name": name, "price": price}

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate):
    return {
        "name": item.name,
        "price": item.price,
        "secret": "hidden"
    }

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    items[item_id] = item.model_dump()
    return items[item_id]

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: ItemUpdate):
    existing_item = items[item_id]

    if item.name is not None:
        existing_item["name"] = item.name

    if item.price is not None:
        existing_item["price"] = item.price

    return existing_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    del items[item_id]
    return {"message": "Item deleted"}