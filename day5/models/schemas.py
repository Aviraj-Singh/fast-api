from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: int

class UserCreate(BaseModel):
    name: str