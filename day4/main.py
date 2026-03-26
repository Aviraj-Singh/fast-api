from fastapi import FastAPI
from routes import items
from exceptions.items import ItemNotFoundException, ItemAlreadyExistsException
from fastapi.responses import JSONResponse
"""
I can import the items like this as well - from day3.routes import items
But in that case I have to run app like uvicorn day3.main:app --reload not uvicorn main:app --reload
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