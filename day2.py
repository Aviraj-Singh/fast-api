"""
Day 2 - Dependency Injection (DI)
• How FastAPI manages dependencies automatically
• Chaining dependencies (dependency inside dependency)
• Built a basic auth flow (token validation)
• How requests can be blocked before reaching routes
"""

from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()

items = {
    1: {"name": "iPhone", "price": 140000},
    2: {"name": "samsung", "price": 150000}
}

def get_items_db():
    return items

def get_token(token: str = Header()):
    return token


def get_current_user(token=Depends(get_token)):
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"user": "Aviraj"}

@app.get("/")
def read_root():
    return {"message": "Server started"}

@app.get("/items")
def read_items(db = Depends(get_items_db)):
    return db

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db=Depends(get_items_db)):
    # Check if the key exists in the dictionary first
    if item_id in db:
        del db[item_id]
        return {"message": f"Item {item_id} deleted"}

    # If it's not there, raise the exception
    raise HTTPException(status_code=404, detail="Item ID not found")

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return user