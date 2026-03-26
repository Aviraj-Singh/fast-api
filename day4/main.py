from fastapi import FastAPI
from routes import items
from exceptions.items import ItemNotFoundException, ItemAlreadyExistsException
from fastapi.responses import JSONResponse
"""
Day 4: Built full CRUD APIs (GET, POST, PUT, DELETE)
"""

app = FastAPI()

app.include_router(items.router)

@app.exception_handler(ItemNotFoundException)
def item_not_found_handler(request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Item not found",
            "item_id": exc.item_id
        }
    )

@app.exception_handler(ItemAlreadyExistsException)
def item_already_exists_handler(request, exc: ItemAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={
            "error": "Item already exists",
            "item_name": exc.item_name
        }
    )