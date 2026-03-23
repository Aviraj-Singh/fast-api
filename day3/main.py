from fastapi import FastAPI
from routes import items, profile
from exceptions.items import ItemNotFoundException
from fastapi.responses import JSONResponse
"""
I can import the items like this as well - from day3.routes import items
But in that case I have to run app like uvicorn day3.main:app --reload not uvicorn main:app --reload
"""

app = FastAPI()

app.include_router(items.router)
app.include_router(profile.router)

@app.exception_handler(ItemNotFoundException)
def item_not_found_handler(request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Item not found",
            "item_id": exc.item_id
        }
    )